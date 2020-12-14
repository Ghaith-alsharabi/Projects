from login import *
from adminEmail import adminEmail
import smtplib
import pyshark
import time
import subprocess
import pyfiglet
import netifaces
import os



def UdpAttack(pkt):
    if pkt.transport_layer=="UDP":
      if int(pkt.ip.len) >=1500:
        subprocess.call(["sudo", "iptables", "-A", "INPUT","-p", "ALL", "-m","mac","--mac-source",str(pkt.eth.src_resolved),"-j","DROP"])
        subprocess.call(["sudo", "iptables", "-A", "FORWARD","-p", "ALL", "-m","mac","--mac-source",str(pkt.eth.src_resolved),"-j","DROP"])
        subprocess.call(["sudo", "iptables", "-A", "OUTPUT","-p", "ALL", "-m","mac","--mac-source",str(pkt.eth.src_resolved),"-j","DROP"])       
        f = open("blackList.txt", "a")
        f.write("#" * 80)
        f.write("\n")
        f.write("Program has blocked the following IP: " + pkt.ip.src + " The attack is detected at " + str(time.ctime(time.time())) +"\n")
        f.write("#" * 80)
        f.write("\n")
        f.close()
        print('udp flood attack')
        #print("Protcol: "+ pkt.highest_layer + "| Src IP: "+ pkt.ip.src+ "| Dest IP: "+ pkt.ip.dst +"| Packet length:" + pkt.ip.len )


def HttpFlood(pkt):
    if (str(pkt.highest_layer) == "TCP"):
        if (str(pkt[pkt.transport_layer].dstport) == "80") and (str(pkt.eth.src) in MACDic):
            MACDic[str(pkt.eth.src)] = MACDic[str(pkt.eth.src)] + str(pkt[pkt.transport_layer].dstport) + ","
    if (str(pkt.highest_layer) == "TCP") and (str(pkt[pkt.transport_layer].dstport) == "80") and (str(pkt.eth.src) not in MACDic):
        MACDic[str(pkt.eth.src)] = str(pkt[pkt.transport_layer].dstport) + ","
    for key in MACDic:
        listOfValues = MACDic[key][:-1].split(",")
        if len(listOfValues) == 200:
            if str(pkt.eth.src) not in blockedMACs1:
                print("User: " + pkt.eth.src + " is HTTP attacking you")
                os.system("sudo iptables -A FORWARD -p ALL -m mac --mac-source " + str(pkt.eth.src) + " -j DROP")
                os.system("sudo iptables -A INPUT -p ALL -m mac --mac-source " + str(pkt.eth.src) + " -j DROP")
                f = open("blackList.txt", "a")
                f.write("User: " + pkt.eth.src + " Has been blocked\n")
                f.close()
                body = pkt.eth.src + " is Attacking. MAC-Address was blocked. Please take action"
                emailContent = "Dear: " + userName + "\nSender's E-mail: " + \
                    encKey.decrypt(email).decode("utf-8") + \
                    "\nE-mail body:\n" + body
                message_final = "Subject: Network Warning\n\n" + emailContent
                mail = smtplib.SMTP("smtp.gmail.com")
                mail.ehlo()
                mail.starttls()
                mail.login(encKey.decrypt(email).decode("utf-8"),encKey.decrypt(passwd).decode("utf-8"))
                mail.sendmail(encKey.decrypt(email).decode("utf-8"), userEmail, message_final)
                mail.quit()
                blockedMACs1.append(str(pkt.eth.src))
            else:
                pass


def Pingod(pkt):
    if pkt.highest_layer == "DATA":
     if int(pkt.ip.len) == 1500:
      if pkt.eth.src not in blockedMACs:
         print("User: " + pkt.eth.src + " is attacking")
         os.system("sudo iptables -A FORWARD -p ALL -m mac --mac-source " + pkt.eth.src + " -j DROP")
         os.system("sudo iptables -A INPUT -p ALL -m mac --mac-source " + pkt.eth.src + " -j DROP")
         body = pkt.eth.src + " is Attacking. MAC-Address was blocked. Please take action"
         emailContent = "Dear: " + userName + "\nSender's E-mail: " + encKey.decrypt(email).decode("utf-8") + "\nE-mail Body:\n" + body
         #message_final = "Subject: {}\n\n{}".format("Network Warning", emailContent)
         message_final = "Subject: Network Warning\n\n" + emailContent
         mail = smtplib.SMTP("smtp.gmail.com", 587)
         mail.ehlo()
         mail.starttls()
         mail.login(encKey.decrypt(email).decode("utf-8"), encKey.decrypt(passwd).decode("utf-8"))
         mail.sendmail(encKey.decrypt(email).decode("utf-8"), adminEmail, message_final)
         mail.quit()
         blockedMACs.append(pkt.eth.src)
         f = open("blackList.txt", "a")
         f.write("Program has blocked the following user: " + pkt.eth.src + "\n")
         f.close()
      else:
         pass

def PortScan(pkt):    
    #packet filter method
    
    #the index of the packet inside the list list_ip
    index=0
    global packets_counter
    #increase the packet counter each time a new packet comes across
    packets_counter+=1
    try:
        #Source IP of the packet
        packet_src=str(pkt.ip.src)
        #check if we have the packet already in our list
        if(packet_src in list_ip):
            #get the index of existing packet
            index=list_ip.index(packet_src)
            #increase packets number for this ip
            traffic[index][1]+=1
            
            #check if the port is already exist for this ip in the list
            if(pkt[pkt.transport_layer].dstport not in traffic[index][2]):
                #add the new port to the list
               traffic[index][2].append(pkt[pkt.transport_layer].dstport)
               
            #in this scenario we suppose that the first three packets are normal(handshake) so 3 packets and one port
            if(traffic[index][1]<=3 and len(traffic[index][2])>1):
               print("Port Scanning warning!!")
               print("Host : ",packet_src," has scanned the following Ports : ",traffic[index][2])
               print(traffic[index][1]," Packets sent..")
               print(len(traffic[index][2])," Ports scanned...")
         #      exit()
            
            #in this scenario we suppose that this ip has already connected to our ip/ we check how many ports this IP is using   
            if(len(traffic[index][2])>=10):
               print("Port Scanning warning!!")
               print("Host : ",packet_src," has scanned the following Ports : ",traffic[index][2])
               print(traffic[index][1]," Packets sent..")
               print(len(traffic[index][2])," Ports scanned...")
               f = open("blackList.txt", "a")
               f.write("#" * 80)
               f.write("\n")
               f.write("This ==> "+ str(pkt.eth.src_resolved) +" has scaned thoese ports ==> "+str(traffic[index][2])+ " The attack is detected at " + str(time.ctime(time.time())) +"\n" )              
               f.write("#" * 80)
               f.write("\n")
               f.close()               
               subprocess.call(["sudo", "iptables", "-A", "INPUT","-p", "ALL", "-m","mac","--mac-source",str(pkt.eth.src_resolved),"-j","DROP"])
               subprocess.call(["sudo", "iptables", "-A", "FORWARD","-p", "ALL", "-m","mac","--mac-source",str(pkt.eth.src_resolved),"-j","DROP"])
               subprocess.call(["sudo", "iptables", "-A", "OUTPUT","-p", "ALL", "-m","mac","--mac-source",str(pkt.eth.src_resolved),"-j","DROP"])

               
              # exit()
               
        else:
            
            #if the packet is not in the list then add it
            list_ip.append(packet_src)
            traffic.append([packet_src,1,[pkt[pkt.transport_layer].dstport]])
            
    except AttributeError:
        pass
    except IndexError:
        pass

def arpPoision(pkt):    
    if "ARP Layer" in str(pkt.layers):
      if pkt.arp.src_proto_ipv4 in arpPoison:
        if str(pkt.arp.src_hw_mac) not in str(arpPoison[pkt.arp.src_proto_ipv4]):
            arpPoison[pkt.arp.src_proto_ipv4].append(pkt.arp.src_hw_mac)    
      else:
         arpPoison[pkt.arp.src_proto_ipv4] = [pkt.arp.src_hw_mac]
   # print(arpPoison[pkt.arp.src_proto_ipv4])
      if len(arpPoison[pkt.arp.src_proto_ipv4]) >=2:
        print("arp spoofing is detected at " + str(time.ctime(time.time())) + "!!!!\n")
        print("This ==> " +arpPoison[pkt.arp.src_proto_ipv4][1]+ " Mac Address is ATTACKING US !!!!!!!!!!!\n")
        subprocess.call(["sudo", "iptables", "-A", "INPUT","-p", "ALL", "-m","mac","--mac-source",str(arpPoison[pkt.arp.src_proto_ipv4][1]),"-j","DROP"])
        subprocess.call(["sudo", "iptables", "-A", "FORWARD","-p", "ALL", "-m","mac","--mac-source",str(arpPoison[pkt.arp.src_proto_ipv4][1]),"-j","DROP"])
  
def DDoS(pkt):   
   global packetDic
   #if the flag is SYN or None then add the mac address to the dic   
   if pkt.transport_layer=="TCP":
        if pkt.tcp.flags.showname[13:] == "(SYN)" or pkt.tcp.flags.showname[13:] == "(<None>)":      
           # if the packet is in the dic then add one to the first index of the list and put the arrived time for this new packet in the thierd index in the list                
            if "Mac address: "+str(pkt.eth.src_resolved) in packetDic:                     
                #add the new packet to the first index of the list 
                packetDic["Mac address: "+str(pkt.eth.src_resolved)][0] += 1
                #add the time to the thierd index of the list 
                packetDic["Mac address: "+str(pkt.eth.src_resolved)][2] = round(time.time())            
        
             #add the maliscios mac address to the dic and put in the list the packet arrived time
            else:
                packetDic["Mac address: "+str(pkt.eth.src_resolved)] = [1, round(time.time()), 0] 
   
        # If the mac address in the dic and the time of the first packet plus 4 is smaller or equal to the current time, 4 seconds will be finished. 
        if "Mac address: "+str(pkt.eth.src_resolved) in packetDic and packetDic["Mac address: "+str(pkt.eth.src_resolved)][1] + 4 <= round(time.time()):
            print("-"*79)
            print("4 sec is finished\n")
        
           #if in this 4 sec this mac address has sent more than 15 (syn or none) packet without ack then print the resultaat and block the mac address         
            if packetDic["Mac address: "+str(pkt.eth.src_resolved)][0] >= 15: 
                for mac, li in packetDic.items():
                    print("This ==> "+ mac +" has sent this amount of packets ==> "+str(li[0]))
                    print("The first packet is detected at " + str(time.ctime(li[1])) + " and the last packet at" +  str(time.ctime(li[2])) +"\n")
                    #put the output in a file  
                    fi = open("blackList.txt", "a")
                    fi.write("This ==> "+ mac +" has sent this amount of packets ==> "+str(li[0])+ "the first packet is detected at " + str(time.ctime(li[1])) + " and the last packet at " +  str(time.ctime(li[2])) +"\n" )              
                    fi.close()
                    print("Block this mac",pkt.eth.src_resolved + "\n")
                    print('-'*79)
            
            #iptables to block the mac address
            subprocess.call(["sudo", "iptables", "-A", "INPUT","-p", "ALL", "-m","mac","--mac-source",str(pkt.eth.src_resolved),"-j","DROP"])
            subprocess.call(["sudo", "iptables", "-A", "FORWARD","-p", "ALL", "-m","mac","--mac-source",str(pkt.eth.src_resolved),"-j","DROP"])
            subprocess.call(["sudo", "iptables", "-A", "OUTPUT","-p", "ALL", "-m","mac","--mac-source",str(pkt.eth.src_resolved),"-j","DROP"])
            
            #Delete the mac address from the dic after blocking him to not having a problem with the memory             
            del packetDic["Mac address: "+str(pkt.eth.src_resolved)]
   
        #if the ack recived and the mac address in the dic then delete the mac address from the dic 
        if pkt.transport_layer=="TCP" and pkt.tcp.flags.showname[13:] == "(ACK)"  and "Mac address: "+str(pkt.eth.src_resolved) in packetDic:
        #ack recived 
            del packetDic["Mac address: "+str(pkt.eth.src_resolved)]     

def main():
    global userName
    userName = "Network Admin"
    global userEmail
    userEmail = adminEmail
    global blockedMACs
    blockedMACs = []
    global blockedMACs1
    blockedMACs1 = []
    global blockedMACs2
    blockedMACs2=[]
    global MACDic
    MACDic = {}
    global list_ip
    list_ip=[]
    global traffic
    traffic=[]
    global packetDic
    packetDic={}
    global packets_counter
    packets_counter=0
    global arpPoison
    arpPoison={}
    ascii_banner = pyfiglet.figlet_format("963 UniT")
    print(ascii_banner)    
    print("Wait")
    cap = pyshark.LiveCapture(interface="wlan0")
    #continuously sniffing
    packet_iterator = cap.sniff_continuously
    print("capturing...")
    #open this file
    
    for pkt in packet_iterator():   
        DDoS(pkt)
        UdpAttack(pkt)
        HttpFlood(pkt)
        Pingod(pkt)
        PortScan(pkt)
        arpPoision(pkt)

if __name__ == '__main__':
    main()