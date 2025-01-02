#include <ros/ros.h>
#include "unitree_legged_sdk/lcm_server.h"
#include "unitree_legged_msgs/HighState.h"
#include "unitree_legged_msgs/HighCmd.h"
#include "convert.h"

using namespace UNITREE_LEGGED_SDK;

class LcmRosBridge {
private:
    ros::NodeHandle nh_;
    ros::Publisher state_pub_;
    ros::Subscriber cmd_sub_;
    LeggedType rname_;
    Lcm_Server_High* server_; 

public:
	    LcmRosBridge(LeggedType rname) : rname_(rname) {
	    std::cout << "Initializing LCM-ROS Bridge..." << std::endl;
	    
	    // Initialize ROS topics
	    state_pub_ = nh_.advertise<unitree_legged_msgs::HighState>("/unitree_legged_msgs/HighState", 10);
	    std::cout << "Created state publisher on: " << state_pub_.getTopic() << std::endl;
	    
	    cmd_sub_ = nh_.subscribe("/unitree_legged_msgs/HighCmd", 10, &LcmRosBridge::cmdCallback, this);
	    std::cout << "Created command subscriber on: /unitree_legged_msgs/HighCmd" << std::endl;
	    std::cout << "Subscriber queue size: " << cmd_sub_.getNumPublishers() << std::endl;

	    std::cout << "Creating UDP connection..." << std::endl;
	    std::cout << "UDP settings:" << std::endl;
		std::cout << " - Client port: " << UDP_CLIENT_PORT << std::endl;
		std::cout << " - Server port: " << UDP_SERVER_PORT << std::endl;
		std::cout << " - Server IP: " << UDP_SERVER_IP_BASIC << std::endl;

		std::cout << "UDP connection created" << std::endl;

// After server initialization:
std::cout << "UDP connection created" << std::endl;
    
	    
	    // Initialize LCM server
	    server_ = new Lcm_Server_High(rname_);
	    server_->mylcm.SubscribeCmd();
	    
	    std::cout << "Bridge initialized, topics created" << std::endl;
	}

    ~LcmRosBridge() {
        if (server_) {
            delete server_;
            server_ = nullptr;
        }
    }

    void run() {//Shows bridge is alive and running
        ROS_INFO("LCM-ROS bridge running...");
        
        // Start LCM loops
        LoopFunc loop_control("control_loop", 0.002, boost::bind(&Lcm_Server_High::RobotControl, server_));
        LoopFunc loop_udpSend("UDP_Send", 0.002, 3, boost::bind(&Lcm_Server_High::UDPSend, server_));
        LoopFunc loop_udpRecv("UDP_Recv", 0.002, 3, boost::bind(&Lcm_Server_High::UDPRecv, server_));
        LoopFunc loop_lcm("LCM_Recv", 0.002, boost::bind(&Lcm_Server_High::LCMRecv, server_));
        
        std::cout << "Starting LCM loops..." << std::endl;
        
        loop_udpSend.start();
        loop_udpRecv.start();
        loop_lcm.start();
        loop_control.start();
        
        std::cout << "All loops started" << std::endl;
        
        ros::Rate rate(500);
        int count = 0;
        while (ros::ok()) {
            if(count++ % 500 == 0) {  // Print every second
		std::cout << "Bridge loop running, iteration: " << count << std::endl;
		std::cout << "Number of command publishers: " << cmd_sub_.getNumPublishers() << std::endl;
	    }
	    publishState();
	    ros::spinOnce();
	    rate.sleep();
	}
    }

private:
    void publishState() { //Shows how often states are being published
        static int pub_count = 0;
        if(pub_count++ % 500 == 0) {  // Print every second
            std::cout << "Publishing state, count: " << pub_count << std::endl;
        }
        
        unitree_legged_msgs::HighState ros_state;
        // Convert LCM state to ROS message
        state_pub_.publish(ros_state);
    }

    void cmdCallback(const unitree_legged_msgs::HighCmd::ConstPtr& msg) {
	    std::cout << "\n=== Received ROS Command ===" << std::endl;
	    std::cout << "Mode: " << (int)msg->mode << std::endl;
	    std::cout << "Forward Speed: " << msg->forwardSpeed << std::endl;
	    std::cout << "Rotate Speed: " << msg->rotateSpeed << std::endl;
	    std::cout << "Body Height: " << msg->bodyHeight << std::endl;
	    
	    // Convert ROS command to LCM and send
	    UNITREE_LEGGED_SDK::HighCmd lcm_cmd;
	    lcm_cmd = ToLcm(*msg, lcm_cmd);
	    server_->mylcm.Send(lcm_cmd);
	    
	    std::cout << "Command sent to LCM" << std::endl;
	    std::cout << "==========================" << std::endl;
	}
};

int main(int argc, char** argv) {
    ros::init(argc, argv, "lcm_ros_bridge");
    
    if (argc != 2) {
        ROS_ERROR("Usage: lcm_ros_bridge <robot_name>");
        return 1;
    }

    LeggedType rname;
    if (strcasecmp(argv[1], "A1") == 0) {
        rname = LeggedType::A1;
    } else {
        ROS_ERROR("Unsupported robot type");
        return 1;
    }

    std::cout << "Starting LCM-ROS bridge node..." << std::endl;
    
    LcmRosBridge bridge(rname);
    bridge.run();
    return 0;
}
