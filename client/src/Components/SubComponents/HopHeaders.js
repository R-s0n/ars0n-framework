import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const HopHeaders = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <p><b>Summary:</b> Adding known Hop-by-Hop Headers to the "Connection:" header values can force misconfigured reverse-proxy servers and/or load balancers to remove these Hop-by-Hop Headers, producing unpredicitable responses.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Bypass access controls</li>
                        <li>Fingerprint back-end technology/services</li>
                        <li>Infer valuable information about how the application processes requests.</li>
                        <li>Produce error messages</li>
                        <li>Bypass WAF (or other defense mechanisms)</li>
                    </ol>
                    <p><b>Methodology - Identifying Vulnerabilities:</b></p>
                    <ol>
                        <li>Check to see if the proxy chain is vulnerable:</li>
                        <ol>
                            <li>Add existing header w/ known functionality (Ex: Cookie) to Connection header values.</li>
                            <li>Send request.</li>
                            <li>Look for changes in request length, status code, or any other aspect of the response.  <b>NOTE: </b>No change does NOT necessarialy mean that the proxy chain is not vulnerable.</li>
                        </ol>
                        <li>Using the same methodology, test any unique headers that are included in the original request (Ex: X-BLUECOAT-VIA).</li>
                        <li>Using the same methodology, bruteforce using a headers wordlist (Ex: SecLists/Discovery/Web-Content/BurpSuite-ParamMiner/lowercase-headers).</li>
                    </ol>
                    <p><b>Methodology - Exploiting Vulnerabilities:</b></p>
                    <ol>
                        <li><b>Bypass access controls:</b> Delete headers that may identify the sender's IP address (MODAL HERE), which may be used for whitelisting resources.</li>
                        <li><b>Fingerprint back-end technology/services:</b> This is something that comes with experience, but here are a few things to consider.</li>
                        <ul>
                            <li>Look for error messages or any chance in the response (length, status code, etc.)</li>
                            <li>If found, research the function of the header being removed.</li>
                            <li>Compare the response time with a normal response to try and find where along the proxy chain the error is being removed.</li>
                        </ul>
                        <li><b>Bypass WAF (or other defense mechanisms):</b> If an application allows clients to send requests to a reverse proxy before routing to a WAF, the proxy may skip this route if certain headers are missing.</li>
                        <ol>
                            <li>Identify WAF that is filtering malicious requests.</li>
                            <li>Identify hop-by-hop header vulnerability.</li>
                            <li>Re-send malicious request w/ hop-by-hop header included in Connection header.</li>
                        </ol>
                    </ol>
                    <p><b>BONUS:</b> Combine this technique w/ an SSRF to potentially increase the impact of the SSRF vuln!</p>
                </div>
            </div>
        </div>
    );

}

export default HopHeaders;