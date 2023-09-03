import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const AwsS3 = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h3 className="pb-3 pt-3">AWS S3 Bucket Misconfiguration</h3>
                    <p><b>Summary:</b> Amazon S3 buckets are scalable and secure storage containers in Amazon Web Services that store and manage data, files, and objects, accessible via unique URLs.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Read sensitive data stored on the S3 bucket</li>
                        <li>Upload malicious files to the S3 bucket</li>
                        <li>Modify the contents of critical data stored on the S3 bucket</li>
                        <li>Delete critical data/files stored on the S3 bucket</li>
                        <li>Exfiltrate backup files containing sensitive data</li>
                        <li>Enumerate hidden S3 bucket names</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default AwsS3;