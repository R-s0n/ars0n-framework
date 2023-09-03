import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const AwsEc2 = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">AWS EC2 Misconfiguration</h3>
                    <p><b>Summary:</b> An AWS EC2 (Elastic Compute Cloud) instance is a virtual server within Amazon Web Services that allows users to rent scalable computing resources, such as processing power and memory, to run applications and services on-demand in the cloud.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Download the Amazon Machine Image (AMI) file of a misconfigured private EC2</li>
                        <li>Brute-force Public URL Templates to potentially bypass security controls</li>
                        <li>Enumerate private EC2 instances misconfigured with a public IP address</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default AwsEc2;