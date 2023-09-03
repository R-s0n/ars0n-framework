import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const AwsIamSts = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">AWS IAM/STS Misconfiguration</h3>
                    <p><b>Summary:</b> AWS IAM (Identity and Access Management) is a service that controls access to AWS resources by managing users, groups, permissions, and authentication. AWS STS (Security Token Service) is a service that provides temporary credentials for accessing AWS resources, helping to enhance security by minimizing the exposure of long-term credentials. AWS IAM sets up user identities and their permissions, while AWS STS issues temporary security tokens to these authenticated users, ensuring secure and limited access to resources without requiring long-term credentials.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Enumerate cross account roles and users without proper authentication/authorization</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default AwsIamSts;