import React from 'react';
import UrlForm from '../HelperComponents/UrlForm';

const EyeWitness = props => {

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <h3>Add Target Urls</h3>
                    <p>Based on the Recon results, add any interesting looking URLs that should be taken to the Enumeration phase.</p>
                </div>
            </div>
            <div className="row">
                <UrlForm thisFqdn={props.thisFqdn} thisScanner="targetUrls"/>
            </div>
        </div>
    )
}

export default EyeWitness;