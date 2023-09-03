import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const AwsExposedDocDb = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">AWS Exposed Sensitive DocumentDB</h3>
                    <p><b>Summary:</b> AWS DocumentDB is a fully managed, scalable NoSQL database service compatible with MongoDB, designed to provide high performance and availability for storing, querying, and managing document-oriented data.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Establish an unauthorized connection to a misconfigured instance of DocumentDB</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default AwsExposedDocDb;