import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const AwsElasticBean = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">AWS Elastic Beanstalk Misconfiguration</h3>
                    <p><b>Summary:</b> AWS Elastic Beanstalk is a Platform-as-a-Service (PaaS) that simplifies the deployment and management of web applications and services. It automatically handles the underlying infrastructure, such as provisioning, scaling, load balancing, and application health monitoring, allowing developers to focus solely on their code.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Gain public access to internal Elastic Beanstalk instances</li>
                        <li>Bypass security/access controls configured through the Elastic Beanstalk</li>
                        <li>Access application code stored on public S3 buckets in Elastic Beanstalk applications</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default AwsElasticBean;