import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const AwsRds = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">AWS RDS Misconfiguration</h3>
                    <p><b>Summary:</b> AWS RDS (Relational Database Service) is a cloud service that simplifies database management by handling tasks like setup, scaling, and maintenance for various relational database engines, letting users concentrate more on building applications.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Establish an unauthorized connection to a misconfigured RDS instance</li>
                        <li>Enumerate and download internal/sensitive RDS snapshots</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default AwsRds;