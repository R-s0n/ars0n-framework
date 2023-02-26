import React from 'react';

import toast, { Toaster } from 'react-hot-toast';
import UrlForm from '../HelperComponents/UrlForm';

const GithubSearch = props => {


    const notify = e => {
        navigator.clipboard.writeText(e.target.innerText)
        toast(`Copied "${e.target.innerText}" to Clipboard`)
    }



    const org = props.thisFqdn.fqdn.replace(".com", "");

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <Toaster />
                    <p><b>DETAILS: </b>A collection of Python, PHP, and Bash scripts used to automate basic GitHub enumeration.</p>
                    <p><b>GOAL: </b>To begin building a basic understanding of an organization's presence on Github and give security researchers resources to build a plan of attack.</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={notify}>sudo git clone https://github.com/gwen001/github-search.git; pip3 install -r requirements2.txt && pip3 install -r requirements3.txt</span></p>
                    <p><b>RUN: </b><ul>
                                        <li>Run checks against wordlist of dorks: <span onClick={notify}>sudo python3 github-dorks.py -o {org} -d dorks.txt -e 10 &gt; dorks.{org}.github-search.txt</span></li>
                                        <li>Search for additional terms not included in wordlist: <span onClick={notify}>sudo php github-search.php -o {org} -s db_password &gt; search.{org}.github-search.txt</span></li>
                                        <li>Search for users associated with an organization: <span onClick={notify}>sudo python3 github-users.py -k {org} &gt; users.{org}.github-search.txt</span></li>
                                        <li>Search for employees associated with an organization: <span onClick={notify}>sudo python3 github-employees.py -m linkedin -t "{org}" -p 3 &gt; employees.{org}.github-search.txt</span></li>
                                    </ul></p>
                </div>
            </div>
            <div className="row">
                <UrlForm thisFqdn={props.thisFqdn} thisScanner="Github"/>
            </div>
        </div>
    )
}

export default GithubSearch;