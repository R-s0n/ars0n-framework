import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const ManualTestingTemplate = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <p><b>Summary:</b></p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li></li>
                    </ol>
                    <p><b>Methodology - Identifying Vulnerabilities:</b></p>
                    <ol>
                        <li></li>
                    </ol>
                    <p><b>Methodology - Exploiting Vulnerabilities:</b></p>
                    <ol>
                        <li></li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default ManualTestingTemplate;