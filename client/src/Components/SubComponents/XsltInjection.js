import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const XsltInjection = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">eXtensible Stylesheet Language Transformations (XSLT) Injection</h3>
                    <p><b>Summary:</b> Extensible Stylesheet Language Transformations (XSLT) is a programming language used for transforming and manipulating XML documents into different formats, such as HTML, text, or other XML structures. It enables developers to define templates and rules to extract and rearrange data from XML documents, facilitating the conversion of data between different representations.</p>
                    <p>The most used frameworks are: Libxslt (Gnome), Xalan (Apache) and Saxon (Saxonica).</p>
                    <p>If an attacker is able to inject malicious XSL tags into a response from a web application that uses XSLT, they can exploit this mechanism to access sensitive files or even execute malicious commands on the target server.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Force the target server to make unintended HTTP requests, resulting in a Server-Side Request Forgery (SSRF)</li>
                        <li>Read the contents of sensitive files on the target server</li>
                        <li>Execute arbitrary commands on the target server, gaining Remote Code Execution (RCE)</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default XsltInjection;