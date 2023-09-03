import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const IpSpoofing = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">IP Address Spoofing</h3>
                    <p><b>Summary:</b> Most reverse proxies capture the IP Address of the client and use that value in some way. In same cases, the proxy will also use header values or other sources to modify the value of the client's IP in some way. If an attacker is able to manipulate this behavior and control their Remote Socket IP Address within the context of the application, they can cause unexpected behavior and potentially bypass security controls.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Bypass brute-force restrictions based on IP Address</li>
                        <li>Access privileged areas within the application restricted by IP Address</li>
                        <li>Access internal applications restricted by IP Address</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default IpSpoofing;