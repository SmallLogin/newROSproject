#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re,socket               # 导入 socket 模块
import sys
sys.path.append("/home/smalllogo/tracking_ws/src/uav_follow_robot/scripts/1209/PyIT2FLS-master/PyIT2FLS-master/examples")
from new_v1 import IT2FL_v1_fun
from new_v2 import IT2FL_v2_fun

# from Send_Control import send_control
 
s = socket.socket()         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port = 12345                # 设置端口号
ADDR = (host, port)

s=socket.socket() 
port=12346
    # global clientsocket
sendsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sendsocket.connect((host,port))



# def send_center(x,y):
#     message = str(str([x])+str([y]))
#     clientsocket.sendall(message.encode('utf-8'))
#     print "Send Success!"

def send_center(x,y):
    # message = str([x])
    message = str([x,y])
    print("Send", message)
    sendsocket.sendall(message.encode('utf-8'))

    
def tcpServer():
    # TCP服务
    # with socket.socket() as s:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 绑定服务器地址和端口
        s.bind(ADDR)
        # 启动服务监听
        s.listen(3)
        print('Waitting for connnecting')
        while True:
            # 等待客户端连接请求,获取connSock
            conn, addr = s.accept()
            print('{} Connected!'.format(addr))
            with conn:
                while True:
                    # 接收请求信息
                    data = conn.recv(1024)
                    if data:
                        endata = data.decode('utf-8')
                        subdata = re.findall(r'\[\d+\]\[\d+\]', endata)
                        if subdata:
                            # if len(subdata) == 0:
                            usefuldata = [int(subdata[0].split('][')[0][1:]), int(subdata[0].split('][')[1][:-1])]
                            print('Received data:', usefuldata)
                            # print('Received data:', usefuldata[1])
                            # Center in usefuldata with list 
                            # Calculate IT2FS
                            # IT2FL_fun(0.8,0.6)
                            w=752
                            h=480
                            
                            y=(usefuldata[1]-h/2)/(h/2)
                            print("v1_input:",y)
                            # IT2FL_v1_fun(y)
                            v1=IT2FL_v1_fun(y)

                            
                            x=(int(usefuldata[0])-w/2)/(w/2)
                            print("x_value:",x)
                            
                            if x > -0.2 and  x < 0.2: 
                                yaw_des=0
                            else: 
                                yaw_des=IT2FL_v2_fun(x)
                                print("v2_input:",yaw_des)
                            # IT2FL_v2_fun(x)
                            
                            

                            # x_des=0
                            # y_des=0
                            # z_des=2
                            
                            # print("test:",yaw_des)
                            
                            # send_center(x_des, y_des,z_des,yaw_des)
                                                 
                            # Send  IT2FS's return value
                            # conn.send(str(yaw_des).encode('utf-8'))
                            send_center(v1,yaw_des)
                            print("Published:",v1,yaw_des)
                       
            s.close()

def main():
    tcpServer()

if __name__ == '__main__':
    # rospy.init_node("riseq_rotors_waypoint_publisher", anonymous = True)
    main()
 
