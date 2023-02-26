import React from 'react';
import {useToasts} from 'react-toast-notifications';

const SubDomainResults = props => {
    const {addToast} = useToasts()

    const deleteSubdomains = (e) => {
        props.resultsFunction();
    }

    const resultsStyle = {
        height: '400px',
        width: '1200px',
        overflowY: 'scroll',
        border: '1px solid black',
        padding: '10px'
    }

    const copyListToClipboard = (e) => {
        let copyString = "";
        props.subdomainList.map((fqdn, i)=>{
            return (copyString += fqdn + "\n")
        })
        navigator.clipboard.writeText(copyString);
        addToast(`Subdomain List copied to Clipboard`, {appearance:'info',autoDismiss:true});
    }

    return (
        <div className="row mt-1">
            <div className="col-12">
                <h5>Results ({props.subdomainList.length}):</h5>
                <div style={resultsStyle}>
                {
                    props.subdomainList.map((subdomain, i)=>{
                        if (subdomain.substring(0,4) === "http") {
                            return (
                                <p key={i} style={{marginBottom:'1px', marginLeft:'15px'}}><a href={subdomain} target="_blank" rel="noreferrer">{subdomain}</a></p>
                            )
                        } else {
                            return (
                                <p key={i} style={{marginBottom:'1px', marginLeft:'15px'}}><a href={'http://' + subdomain} target="_blank" rel="noreferrer">{subdomain}</a></p>
                            )
                        }
                    })
                }
                </div>
            </div>
            <div className="col-4 mt-2">
                <button className="btn btn-primary" onClick={deleteSubdomains}>Delete</button>
                <button className="btn btn-primary ml-5" onClick={copyListToClipboard}>Copy</button>
            </div>
        </div>
    )
}

export default SubDomainResults;