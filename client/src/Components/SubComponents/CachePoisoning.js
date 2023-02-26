import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const CachePoisoning = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <p><b>Summary:</b> Web Cache Poisoning occurs when the attacker forces the web cache to <strong>store malicious content and serve that malicious content to victim clients</strong>.  Web Cache Poisoning is more a means of delivering attacks instead of an attack itself, and can be used to build impact for vulnerabilities like XSS.</p>
                    <p><b>Goal(s):</b> Web Cache Poisoning is accomplished in two phases:</p>
                    <ol>
                        <li>Force the application to send a response that includes a dangerous payload (Ex: XSS).</li>
                        <li>Cache the malicious response and force the victim to access the malicious response from the web cache.</li>
                    </ol>
                    <p><b>Methodology - Identifying Vulnerabilities:</b></p>
                    <ol>
                        <li>Identify all unkeyed inputs (Ex: Headers -- <strong><i>The X-Forwarded-Host header is often unkeyed</i></strong>).  Remember to use a cache buster, like a unique parameter, to ensure other users aren't served a poisoned page from the cache while testing.  BurpSuite's Param Miner extension can be used for automated testing:</li>
                        <ol>
                            <li>Right-click the request to test.</li>
                            <li>Select "Guess Headers"</li>
                        </ol>
                        <li>Based on the way the application processes the unkeyed input, use this input to produce a malicious response (Ex: Reflected input -&gt; XSS).</li>
                        <li>Cache the malicious response.  There are several variables that can effect whether a response is cached.  Identifying and controlling these variables will come with experience.</li>
                    </ol>
                    <p><b>Methodology - Exploiting Vulnerabilities:</b></p>
                    <p><i>Note that once a web cache poisoning vulnerability has been identified, exploiting the vulnerability is done simply by delivering the url to the victim.  With that being said, web cache poisoning can take many forms.  The following are some examples of those use cases and how to exploit them.</i></p>
                    <ul>
                        <li>Deliver a XSS payload:</li>
                        <ol>
                            <li>Find reflected input.</li>
                            <li>Build working XSS payload through unkeyed input.</li>
                            <li>Cache response with XSS payload.</li>
                        </ol>
                        <li>Deliver an open redirect vulnerability.</li>
                        <li>Exploit unsafe handling of resources (Ex: JavaScript files):</li>
                    </ul>
                </div>
            </div>
        </div>
    );

}

export default CachePoisoning;