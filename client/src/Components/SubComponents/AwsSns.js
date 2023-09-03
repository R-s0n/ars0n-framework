import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const AwsSns = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">AWS SNS Misconfiguration</h3>
                    <p><b>Summary:</b> AWS SNS (Simple Notification Service) is a fully managed messaging service that enables the sending of notifications and alerts to a variety of endpoints, such as email, SMS, and application endpoints.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Bypass access control restrictions to Publish or Subscribe to an internal SNS topic</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default AwsSns;