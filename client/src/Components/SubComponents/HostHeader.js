import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const HostHeader = props => {

    return (
        <div className="container mt-2" style={{overflowX: 'scroll', overflowY: 'scroll', height: '95%', padding: '10px'}}>
            <div className="row">
                <div className="col-12">
                    <p><b>Summary:</b> The HTTP Host Header is used by web servers, reverse proxies, and load balancers to route HTTP requests sent to an IP address to a specific application identified by an FQDN.  Misconfigurations in how the HTTP Host Header is handled can be exploited in a variety of ways.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Discover hidden applications.</li>
                        <li>Leverage misconfigurations to execute a web cache poisoning attack.</li>
                        <li>Find buisness logic flaws and/or authentication bypass vulnerabilities.</li>
                        <li>Leverage misconfigurations to execute a Server-Side Request Forgery (SSRF) attack.</li>
                        <li>Client-side vulnerabilities resulting from a reflected host header (XSS, SSTI, HTMLi, etc.)</li>
                        <li>Server-side injection vulnerabilities resulting from the host header being passed to database queries (SQLi, NoSQLi, etc.)</li>
                    </ol>
                    <p><b>Methodology - Identifying Vulnerabilities:</b></p>
                    <ol>
                        <li>Change the Host Header to an arbitrary value and look for changes in the response.</li>
                        <p className="mt-3"><i>If you can still access the application w/ an arbitrary value in the Host Header:</i></p>
                        <ul>
                            <li>The server may default to your target app when an unrecoginized domain name is sent.</li>
                            <li>You can now work to identify what the host header does (if anything) and how it can be exploited.</li>
                        </ul>
                        <p className="mt-3"><i>If you cannot access the application w/ an arbitrary value in the Host Header:</i></p>
                        <ul>
                            <li>Did the server respond with "Invalid Host header"?</li>
                            <li>Was the request blocked due to security controls?</li>
                            <li>Can you add a non-numeric port? (Host: vulnerable-website.com:bad-stuff-here)</li>
                            <li>How can you manipulate the header to bypass controls? (think SSRF)</li>
                        </ul><br></br>
                        <li>Change the Host Header to specific values known to exploit misconfigurations:</li>
                        <ol className="mt-3">
                            <li>Send duplicate Host Headers:</li>
                            <p className="mt-2 ml-4">GET /example HTTP/1.1<br></br>
                                Host: vulnerable-website.com<br></br>
                                Host: bad-stuff-here</p>
                            <li>Send an absolute URL in the request line:</li>
                            <p className="mt-2 ml-4">GET https://vulnerable-website.com/ HTTP/1.1<br></br>
                                Host: bad-stuff-here</p>
                            <li>Use spacing to bypass validation filters (<i>Note the space before the first Host Header in the example below</i>):</li>
                            <p className="mt-2 ml-4">GET /example HTTP/1.1<br></br>
                                &nbsp;Host: bad-stuff-here<br></br>
                                Host: vulnerable-website.com</p>
                        </ol>
                        <li>Test for other headers that may be used in place of the Host Header for the same workflows (Automate using Burp Param Miner):</li>
                        <ul style={{listStyleType: "none"}}>
                            <li>X-Forwarded-Host</li>
                            <li>X-Host</li>
                            <li>X-Forwarded-Server</li>
                            <li>X-HTTP-Host-Override</li>
                            <li>Forwarded</li>
                        </ul>
                    </ol>
                    <p><b>Methodology - Exploiting Vulnerabilities:</b></p>
                    <ol>
                        <li>Add Later...</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default HostHeader;