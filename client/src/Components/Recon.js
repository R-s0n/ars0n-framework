import React, {useState} from 'react';

import Sublist3r from './SubComponents/Sublist3r';
import Amass from './SubComponents/Amass';
import Assetfinder from './SubComponents/Assetfinder';
import Gau from './SubComponents/Gau';
import Ctl from './SubComponents/Ctl';
import Consolidator from './SubComponents/Consolidator';
import Httprobe from './SubComponents/Httprobe';
import EyeWitness from './SubComponents/EyeWitness';
import Shosubgo from './SubComponents/Shosubgo';
import Subfinder from './SubComponents/Subfinder';
import GithubSubdomains from './SubComponents/GithubSubdomains';
import GoSpider from './SubComponents/GoSpider';
import Hakrawler from './SubComponents/Hakrawler';
import SubDomainizer from './SubComponents/SubDomainizer';
import CloudRanges from './SubComponents/CloudRanges';
import Dnmasscan from './SubComponents/Dnmasscan';
import ShuffleDnsMassive from './SubComponents/ShuffleDnsMassive';
import ShuffleDnsCustom from './SubComponents/ShuffleDnsCustom';
import CustomWordlist from './SubComponents/CustomWordlist';
import FindWebServer from './SubComponents/FindWebServer';
import AddTargetUrl from './SubComponents/AddTargetUrl';
import GithubBruteDork from './SubComponents/GithubBruteDork';
import '../Component.css';

const Recon = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <div className="container-fluid">
            <div className="row">
        <div className="bg-secondary checklistStyle pt-4 ml-4 col-3">
            <ul>
                <li>Subdomain Enumeration</li>
                <ul>
                    <li>Subdomain Scraping</li>
                    <ul>
                        <li onClick={(e)=>setCurrentStep(0)}>Tool - Sublist3r</li>
                        <li onClick={(e)=>setCurrentStep(1)}>Tool - Amass</li>
                        <li onClick={(e)=>setCurrentStep(2)}>Tool - Assetfinder</li>
                        <li onClick={(e)=>setCurrentStep(3)}>Tool - GetAllUrls (gau)</li>
                        <li onClick={(e)=>setCurrentStep(4)}>Certificate Transparency Logs</li>
                        <li onClick={(e)=>setCurrentStep(5)}>Tools - Shosubgo</li>
                        <li onClick={(e)=>setCurrentStep(6)}>Tools - Subfinder</li>
                        <li onClick={(e)=>setCurrentStep(7)}>Tools - Github-Subdomains</li>
                    </ul>
                    <li>Link / JS Discovery</li>
                    <ul>
                        <li onClick={(e)=>setCurrentStep(9)}>Tool - GoSpider</li>
                        <li onClick={(e)=>setCurrentStep(10)}>Tool - Hakrawler</li>
                        <li onClick={(e)=>setCurrentStep(11)}>Tool - SubDomainizer</li>
                    </ul>
                    <li>Subdomain Bruteforcing</li>
                    <ul>
                        <li onClick={(e)=>setCurrentStep(12)}>ShuffleDNS - Massive Wordlist</li>
                        <li onClick={(e)=>setCurrentStep(13)}>Build Custom Wordlist</li>
                        <li onClick={(e)=>setCurrentStep(14)}>ShuffleDNS - Custom Wordlist</li>
                    </ul>
                    <li>Server/Port Enumeration</li>
                    <ul>
                        <li onClick={(e)=>setCurrentStep(15)}>Cloud Ranges</li>
                        <li onClick={(e)=>setCurrentStep(16)}>Dnmasscan</li>
                        <li onClick={(e)=>setCurrentStep(17)}>Identify Web Servers</li>
                    </ul>
                </ul>
                <li>Final Analysis</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(18)}>Build List of Unique Subdomains</li>
                    <li onClick={(e)=>setCurrentStep(19)}>Check SubDomain Status - Httpprobe</li>
                    <li onClick={(e)=>setCurrentStep(20)}>Final Analysis - EyeWitness</li>
                </ul>
                <li onClick={(e)=>setCurrentStep(21)}>Add Target URL</li>
                <li onClick={(e)=>setCurrentStep(22)}>Github Brute Dork</li>
                <li>Summary</li>
            </ul>
        </div>
        <div className="bg-secondary workTableStyle col-8">
            {
                currentStep === 0 ?
                <Sublist3r thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 1 ?
                <Amass thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 2 ?
                <Assetfinder thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 3 ?
                <Gau thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 4 ?
                <Ctl thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 5 ?
                <Shosubgo thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 6 ?
                <Subfinder thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 7 ?
                <GithubSubdomains thisFqdn={props.thisFqdn} /> :
                ''
            }

            {
                currentStep === 9 ?
                <GoSpider thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 10 ?
                <Hakrawler thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 11 ?
                <SubDomainizer thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 12 ?
                <ShuffleDnsMassive thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 13 ?
                <CustomWordlist thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 14 ?
                <ShuffleDnsCustom thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 15 ?
                <CloudRanges thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 16 ?
                <Dnmasscan thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 17 ?
                <FindWebServer thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 18 ?
                <Consolidator thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 19 ?
                <Httprobe thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 20 ?
                <EyeWitness thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 21 ?
                <AddTargetUrl thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 22 ?
                <GithubBruteDork thisFqdn={props.thisFqdn} /> :
                ''
            }
        </div>
        </div>
        </div>
    )
}

export default Recon;