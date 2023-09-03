import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const AwsCognito = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">AWS Cognito Misconfiguration</h3>
                    <p><b>Summary:</b> AWS Cognito is a fully managed service that provides authentication, authorization, and user management for web and mobile applications. It allows developers to easily add user sign-up and sign-in functionality, as well as integrate with third-party identity providers like Google, Facebook, and Amazon.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Enumerate Identity Pool IDs, which can be relatively easy to find, to exploit IAM roles assigned to both unauthenticated users and authenticated users accessing the Identity Pool, allowing them to abuse the associated privileges.</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default AwsCognito;