import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const AwsApiGateway = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">AWS API Gateway Misconfiguration</h3>
                    <p><b>Summary:</b> AWS API Gateway is a managed service that enables the creation, deployment, and management of RESTful APIs to securely connect and expose backend services and functions for applications.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Bypass restrictions on API endpoints by abusing logic flaws in the IAM Syntax for access controls</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default AwsApiGateway;