# verizon-quantum-gateway-set-dns
Access the router API to view and change settings, in particular changing the DNS server.

# Goal 
I created this script because of frustrations at the number of steps required when I needed
to temporarily bypass my pi-hole.  With my Verizon Quantum Gateway router, I had to 
navigate to the router settings, enter the password, then click through a bunch of screens
before getting to the router settings that allowed me to change the secondary dns server to
something real.  When I was ready to use the pi-hole again, I had to do the same steps to
set the secondary dns server to something invalid (thus avoiding bypass of the pi-hole).
This seemed ridiculous.

# Methodology
I borrowed from other codebases to see how to login to the router api remotely:
  - https://github.com/cisasteelersfan/quantum_gateway
  - https://github.com/matray/quantum_gateway_reverse_engineering
  
Verizon does not provide any documentation of the API that I was able to find.  In order
to know the correct API calls and format to update the DNS severs, I used Chrome's 
developer tools to capture network activity while I logged into the router and went to
the appropriate settings and changed the secondary dns server.  Armed with this information,
I made a simple class and scripts that use it to restore or remove a valid secondary
dns server.  The class could easily be extended to control other router functionality by
using the same method of capturing network activity through the router gui, then using the
resulting api calls.

I tried to make this useful, but didn't spend the time looking at best practices on everything
(e.g. is there a smart way to add the self-signed certificate of one's router, instead of
avoiding warnings and verification).  Feel free to improve it or make suggestions.

I am using pyinstaller to generate executables for these scripts so that my wife can run
the restore_dns easily in case of any home internet interruption due to some issue with the
pi-hole.  When I am around, I can quickly switch back and forth to see if I have fixed the issue.
