# C Headers 

I needed a quick way to parse C Code and produce the header definitions. 

I thought this would be easy with some code formatter - but it seems there is nothing around.

I found a post on Stackpverflow regarding using ctags ... 

Specifically the command is 

```bash 
ctags -x --c-kinds=fp <filename>
```

The output is very good - example here slightly abbreviated.

```text
DisplayINP3RIF   function   3251 ax25.c           UCHAR * DisplayINP3RIF(UCHAR * ptr1, UCHAR * ptr2, unsigned int msglen)
DisplayINP3RIF   prototype  2361 ax25.c           UCHAR * DisplayINP3RIF(UCHAR * ptr1, UCHAR * ptr2, unsigned int msglen);
IntDecodeFrame   function   2482 ax25.c           int IntDecodeFrame(MESSAGE * msg, char * buffer, time_t Stamp, UINT Mask, BOOL APRS, BOOL MINI)
IntDecodeFrame   prototype  2470 ax25.c           int IntDecodeFrame(MESSAGE * msg, char * buffer, time_t Stamp, UINT Mask, BOOL APRS, BOOL MCTL);
add_incoming_mycalls function   1179 ax25.c           boolean add_incoming_mycalls(void * socket, char * src_call)
add_raw_frames   function   1013 ax25.c           int add_raw_frames(int snd_ch, string * frame, TStringList * buf)
ax25_info_init   function   1961 ax25.c           void ax25_info_init(TAX25Port * AX25Sess)
```

And if you have short (maybe less than 100 character functions, then you could probably just post-process this file.

However, the code I was parsing seemed to have some rather long definitions, which required a little more massaging before they would be accessable. 

## How to use 

Copy the python code - create a symbol (I have not bothered writing an install script) like this 

```bash
ch='python /Users/Bob/Dev/Python/C_Header/ch.py'
```

To see the output just 

    ch ax25.c 

you will see something like 


```text
command is ctags -x --c-kinds=fp ax25.c > t.t
result is CompletedProcess(args=['ctags -x --c-kinds=fp ax25.c > t.t'], returncode=0, stdout='', stderr='')
Output generated
           int APRSDecodeFrame(MESSAGE * msg, char * buffer, time_t Stamp, UINT Mask); /*function detected */
           int ConvFromAX25(unsigned char * incall, char * outcall); /*function detected */
           BOOL ConvToAX25(char * callsign, unsigned char * ax25call); /*function detected */
           int CountBits(unsigned long in); /*function detected */
           char * DISPLAYARPDATAGRAM(UCHAR * Datagram, UCHAR * Output); /*function detected */
```

You can clean this output up by modifyling the command to 

```bash
ch ax25.c | sort | uniq | grep "(" > ax25.h 
```

# Possible Issues 

The generator does not add in any extra include files, nor does it extract and typedef, defines etc ... This is a purly function header builder (assistant).

It outputs the temporary data to a file called *t.t* - this should probably be created using a tempfile function - but I was in a hurry. The file is removed eah invocation of the code.

## Code Base

Developed on Python 3.10 
