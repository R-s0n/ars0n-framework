import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const HttpRequestSmuggling = props => {

    return (
        <div className="container mt-3 ml-5 mr-0" style={{overflowX: 'scroll', overflowY: 'scroll', height: '95%', padding: '10px'}}>
            <div className="row">
                <div className="col-12">
                    <p><b>Summary:</b> HTTP Request Smuggling occurs when the attacker sends a specially crafted request that causes the front-end proxies and back-end servers to desynchronize.  This vulnerablity occurs when the front-end proxies interpret the request as a single request while the back-end servers interpret it as two separate requests (or vice versa).</p>
                    <p><b>Variations:</b></p>
                    <ul style={{listStyleType: "none"}}>
                        <li><b>CL.TE</b> -- The front-end server uses the Content-Length header and the back-end server uses the Transfer-Encoding header.</li>
                        <li><b>TE.CL</b> -- The front-end server uses the Transfer-Encoding header and the back-end server uses the Content-Length header.</li>
                        <li><b>TE.TE</b> -- The front-end and back-end servers both support the Transfer-Encoding header, but one of the servers can be induced not to process it by obfuscating the header in some way.</li>
                    </ul>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Byass front-end security controls (Ex: Access /admin endpoint that would normally return a 403).</li>
                        <li>Reveal changes the front-end makes to incoming requests.</li>
                        <li>Capture the requests of other users.</li>
                        <li>Increase the impact of reflected XSS by using HTTP request smuggling to deliver the XSS payload.</li>
                        <li>Increase the impact of an internal open-redirect to a wide-open redirect.</li>
                        <li>Leverage HTTP request smuggling to perform web cache poisoning/deception.</li>
                    </ol>
                    <p><b>Methodology - Identifying Vulnerabilities:</b></p>
                    <ol>
                        <li>Use the HTTP Smuggle Probe extension to identify potentially vulnerable URLs.</li>
                        <li>If a potentially vulnerable URL is found, use the following methodology depending on the variation identified:</li>
                        <ul style={{listStyleType: "none"}}>
                            <li><b>CL.TE</b></li>
                            <ol>
                                <li>Manual -- Add G following the chunk size value of zero (<i>Update Content-Length: Enabled</i>)</li>
                                <p><code>Transfer-Encoding: chunked\r\n<br></br>\r\n<br></br>0\r\n<br></br>\r\n<br></br>G</code></p>
                                <li>Burp Extension -- Set prefix to "G"</li>
                                <p><code>prefix = '''G'''</code></p>
                            </ol>
                            <li><b>TE.CL</b></li>
                            <ol>
                                <li>Manual -- Add G following the chunk size value of zero (<i>Update Content-Length: Disabled</i>)</li>
                                <p><code>Content-Length: 4\r\n<br></br>Transfer-Encoding: chunked\r\n<br></br>\r\n<br></br>5a\r\n<br></br>PUT / HTTP/1.1\r\n<br></br>Content-Type: application/x-www-form-urlencoded\r\n<br></br>Content-Length: 15\r\n<br></br>\r\n<br></br>x=1\r\n<br></br>0\r\n<br></br>\r\n<br></br>\r\n</code></p>
                                <li>Burp Extension -- Set prefix to an additional HTTP request that will be processed separately by the front-end server.</li>
                                <p><code>prefix = '''PUT / HTTP/1.1<br></br>
                                        Content-Type: application/x-www-form-urlencoded<br></br>
                                        Content-Length: 15<br></br>
                                        <br></br>
                                        x=1'''<br></br>
                                        </code></p>
                            </ol>
                            <li><b>TE.TE</b></li>
                            <ol>
                                <li>Identify which server is not processing the Transfer-Encoding header correctly (Front-end = CL.TE | Back-end = TE.CL).</li>
                                <li>Use methodology listed above to exploit.</li>
                            </ol>
                        </ul>
                    </ol>
                    <p><b>Methodology - Exploiting Vulnerabilities:</b></p>
                    <ol>
                        <li>This will be added later...</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default HttpRequestSmuggling;