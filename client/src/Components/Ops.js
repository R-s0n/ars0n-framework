import React, {useState} from 'react';

import '../Component.css';
import HopHeaders from './SubComponents/HopHeaders';
import CachePoisoning from './SubComponents/CachePoisoning';
import CacheDeception from './SubComponents/CacheDeception';
import HttpRequestSmuggling from './SubComponents/HttpRequestSmuggling';
import H2cSmuggling from './SubComponents/H2cSmuggling';
import HostHeader from './SubComponents/HostHeader';
import XsltInjection from './SubComponents/XsltInjection';
import EslInjection from './SubComponents/EsiInjection';
import IpSpoofing from './SubComponents/IpSpoofing';
import AwsS3 from './SubComponents/AwsS3';
import AwsCloudfront from './SubComponents/AwsCloudfront';
import AwsIamSts from './SubComponents/AwsIamSts';
import AwsCognito from './SubComponents/AwsCognito';
import AwsExposedDocDb from './SubComponents/AwsExposedDocDb';
import AwsEc2 from './SubComponents/AwsEc2';
import AwsRds from './SubComponents/AwsRds';
import AwsElasticBean from './SubComponents/AwsElasticBean';
import AwsApiGateway from './SubComponents/AwsApiGateway';
import AwsSns from './SubComponents/AwsSns';



const Ops = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <div className="container-fluid">
            <div className="row">
        <div className="bg-secondary checklistStyle pt-2 ml-4 col-3">
        <h4 className="ml-3 pt-2">Infrastructure & DevOps Testing</h4>
            <ul style={{listStyleType: "none"}}>
                <li style={{fontWeight: "bold"}}>Reverse Proxy Testing</li>
                <ul style={{listStyleType: "none"}}>
                    <li onClick={(e)=>setCurrentStep(0)}>Abusing Hop-by-Hop Headers</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Web Cache Poisoning</li>
                    <li onClick={(e)=>setCurrentStep(2)}>Web Cache Deception</li>
                    <li onClick={(e)=>setCurrentStep(3)}>HTTP Request Smuggling</li>
                    <li onClick={(e)=>setCurrentStep(4)}>H2C Smuggling</li>
                    <li onClick={(e)=>setCurrentStep(5)}>XSLT Server-Side Injection</li>
                    <li onClick={(e)=>setCurrentStep(6)}>Edge Side Inclusion (ESI) Injection</li>
                    <li onClick={(e)=>setCurrentStep(7)}>Host Header Poisoning</li>
                    <li onClick={(e)=>setCurrentStep(8)}>IP Address Spoofing</li>
                </ul>
                <li style={{fontWeight: "bold"}}>Cloud-Specific Testing</li>
                <ul style={{listStyleType: "none"}}>
                    <li onClick={(e)=>setCurrentStep(9)}>AWS S3 Bucket Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(10)}>AWS Cloudfront Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(11)}>AWS IAM/STS Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(12)}>AWS Elastic Beanstalk Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(13)}>AWS API Gateway Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(14)}>AWS Cognito Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(15)}>AWS Exposed Sensitive DocumentDB</li>
                    <li onClick={(e)=>setCurrentStep(16)}>AWS EC2 Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(17)}>AWS SNS Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(18)}>AWS RDS Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(19)}>Azure Tenate Enumeration</li>
                    <li onClick={(e)=>setCurrentStep(20)}>Azure User Enumeration</li>
                    <li onClick={(e)=>setCurrentStep(21)}>Azure Open Storage</li>
                    <li onClick={(e)=>setCurrentStep(22)}>Azure Brute-force Credentials</li>
                    <li onClick={(e)=>setCurrentStep(23)}>Azure ACR Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(24)}>Azure App Service Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(25)}>GCP Public Bucket Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(26)}>GCP GitHub Actions</li>
                </ul>
                <li style={{fontWeight: "bold"}}>Web Server Testing</li>
                <ul style={{listStyleType: "none"}}>
                    <li onClick={(e)=>setCurrentStep(27)}>Common Vulnerabilities and Enumerations (CVE's)</li>
                    <li onClick={(e)=>setCurrentStep(28)}>Exposed Configuration Files</li>
                    <li onClick={(e)=>setCurrentStep(29)}>Server Side Includes (SSI) Injection</li>
                    <li onClick={(e)=>setCurrentStep(30)}>Information Disclosure</li>
                </ul>
                <li style={{fontWeight: "bold"}}>Domain Name System (DNS) Testing</li>
                <ul style={{listStyleType: "none"}}>
                    <li onClick={(e)=>setCurrentStep(31)}>DNS Rebinding</li>
                    <li onClick={(e)=>setCurrentStep(32)}>Subdomain Takeover</li>
                </ul>
            </ul>
        </div>
        <div className="bg-secondary workTableStyle col-8">
            {
                currentStep === 0 ?
                <HopHeaders thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 1 ?
                <CachePoisoning thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 2 ?
                <CacheDeception thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 3 ?
                <HttpRequestSmuggling thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 4 ?
                <H2cSmuggling thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 5 ?
                <XsltInjection thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 6 ?
                <EslInjection thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 7 ?
                <HostHeader thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 8 ?
                <IpSpoofing thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 9 ?
                <AwsS3 thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 10 ?
                <AwsCloudfront thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 11 ?
                <AwsIamSts thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 12 ?
                <AwsElasticBean thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 13 ?
                <AwsApiGateway thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 14 ?
                <AwsCognito thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 15 ?
                <AwsExposedDocDb thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 16 ?
                <AwsEc2 thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 17 ?
                <AwsSns thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 18 ?
                <AwsRds thisFqdn={props.thisFqdn} /> :
                ''
            }  
        </div>
        </div>
        </div>
    )
}

export default Ops;