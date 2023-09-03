import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const EslInjection = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">Edge Side Inclusion (ESL) Injection</h3>
                    <p><b>Summary:</b> Edge-Side Includes (ESI) is a web acceleration standard that enables dynamic content assembly at the edge of a content delivery network (CDN). It allows different components of a web page to be fetched and combined in real-time from various sources, improving page load times and reducing the load on the origin server.</p>
                    <p>Edge Side Includes (ESI) requests are processed by a content delivery network (CDN) server, specifically at the Load Balancers of the CDN. If an attacker is able to inject an ESI element into a response from a web application that uses ESI, they can exploit this mechanism to access sensitive files or even execute malicious commands on the target server.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Steal valid cookies from a target victim to gain privilege escalation and/or unauthorized access to the victim's account</li>
                        <li>Read Environmental Variables used on the target server</li>
                        <li>Read the contents of sensitive files on the target server</li>
                        <li>Execute arbitrary commands on the target server, gaining Remote Code Execution (RCE)</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default EslInjection;