import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const AwsCloudfront = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">AWS CloudFlont Misconfiguration</h3>
                    <p><b>Summary:</b> AWS CloudFront is a content delivery service provided by Amazon Web Services in collaboration with Cloudflare, designed to distribute and accelerate content, videos, applications, and APIs to users globally with low latency and high transfer speeds.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Deliver content from a malicious AWS CloudFront instance owned by the attacker, taking advantage of an old DNS record to gain a Subdomain Takeover.</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default AwsCloudfront;