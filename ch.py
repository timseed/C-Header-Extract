import sys
import subprocess 
import os
from pprint import pprint


def get_ctag_data(cmd:str):
    try:
        os.remove('t.t',missing_ok=True)
    except Exception:
        donotcare=1
    result = subprocess.run([cmd], shell=True, capture_output=True, text=True)
    return result

def parse_ctag_output(filename:str,source_file:str):
    with open(filename,"rt") as ifp:
        source=ifp.read()
        lines=source.split('\n')
        for l in lines:
            if len(l)>1: 
                # A Typical line looks like this 
                # get_addr         function    847 ax25.c           int get_addr(char * Calls, UCHAR * AXCalls)
                (functname,ftype,line,file,fdef) = l.strip().split()[:5]
                line=int(line)
                #print(f"FName {functname}")
                #print(f"line  {line}")
                # we need to position of the file .... in the line 
                pos=l.find(file)
                if pos!=-1:
                    #print(f"pos is {pos}")
                    code = l[pos+len(file):]
                    #print(f"Code is {code}")

                    if code.count('(')==code.count(')'):
                        junk=1
                        # Should be a complete definitition
                        if ftype=="function":
                           print(f"{code}; /*function detected */")
                        else:
                            print(f"{code} /*prototype detected */")
                    else:
                        # We want the data after the file 
                        # We get the partial definition and then go and search in the source file

                        fpos = l.find(file)
                        fdef_to_find = l[fpos+len(file):].strip()
                        #print(f"We are looking for {fdef_to_find}")
                        
                        with open(source_file,'rt',errors='ignore') as ifp:
                            sourcefile=ifp.read()
                        fstart=sourcefile.find(fdef_to_find)
                        fnext=fstart+len(fdef_to_find)
                        # Find next ) in code ... Could be an issue if heavy casting is involved
                        fclose=sourcefile[fstart+len(fdef_to_find):].find(')')
                        header=sourcefile[fstart:fstart+len(fdef_to_find)+fclose+1]
                        if header.find(';')!=-1:
                            print(f"{header} /* From Source */")
                        else:
                            print(f"{header}; /* From Source */")







if __name__ == "__main__":
    argc = len(sys.argv)
    if (argc<2):
        print("Need a filename")
        exit()

    file = sys.argv[1]
    cmd=f"ctags -x --c-kinds=fp {file} > t.t"
    print(f"command is {cmd}")
    res = get_ctag_data(cmd)
    print(f"result is {res}")
    if os.path.isfile("t.t"):
        print("Output generated")
        parse_ctag_output("t.t",file)

    else:
        pass
