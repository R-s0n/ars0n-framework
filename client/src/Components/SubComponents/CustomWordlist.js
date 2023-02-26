import React from 'react';

import toast, { Toaster } from 'react-hot-toast';


const CustomWordlist = props => {



    const notify = e => {
        navigator.clipboard.writeText(e.target.innerText)
        toast(`Copied "${e.target.innerText}" to Clipboard`)
    }
    


    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <Toaster />
                    <p><b>DETAILS: </b>CeWL is a ruby app which spiders a given url to a specified depth, optionally following external links, and returns a list of words which can then be used for password crackers such as John the Ripper.</p>
                    <p><b>GOAL: </b>Build a custom wordlist to use for subdomain brute forcing</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={notify}>sudo apt-get install cewl</span></p>
                    <p><b>RUN: </b><span onClick={notify}>cewl -d 2 -m 5 -o -a -w ~/Wordlists/custom.txt https://{props.thisFqdn.fqdn}</span></p>
                </div>
            </div>
        </div>
    )
}

export default CustomWordlist;