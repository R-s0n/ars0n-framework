import React, {useState} from 'react';
import {ToastProvider} from 'react-toast-notifications';
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
        <>
        <div className="bg-secondary checklistStyle pt-4 ml-4">
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
        <div className="bg-secondary workTableStyle">
            {
                currentStep === 0 ?
                <ToastProvider><Sublist3r thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 1 ?
                <ToastProvider><Amass thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 2 ?
                <ToastProvider><Assetfinder thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 3 ?
                <ToastProvider><Gau thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 4 ?
                <ToastProvider><Ctl thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 5 ?
                <ToastProvider><Shosubgo thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 6 ?
                <ToastProvider><Subfinder thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 7 ?
                <ToastProvider><GithubSubdomains thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }

            {
                currentStep === 9 ?
                <ToastProvider><GoSpider thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 10 ?
                <ToastProvider><Hakrawler thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 11 ?
                <ToastProvider><SubDomainizer thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 12 ?
                <ToastProvider><ShuffleDnsMassive thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 13 ?
                <ToastProvider><CustomWordlist thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 14 ?
                <ToastProvider><ShuffleDnsCustom thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 15 ?
                <ToastProvider><CloudRanges thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 16 ?
                <ToastProvider><Dnmasscan thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 17 ?
                <ToastProvider><FindWebServer thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 18 ?
                <ToastProvider><Consolidator thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 19 ?
                <ToastProvider><Httprobe thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 20 ?
                <ToastProvider><EyeWitness thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 21 ?
                <AddTargetUrl thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 22 ?
                <ToastProvider><GithubBruteDork thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
        </div>
        </>
    )
}

export default Recon;