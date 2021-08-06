import React, { useState } from 'react';
import { Step1 } from './steps/Step1';
import { Step2 } from './steps/Step2';
import { formMode } from '../Constants';

export const ContentFormMaster = () => {
    const initialStep = 1;

    const container = document.getElementById('root');

    const [mode, ] = useState(parseInt(container.getAttribute('mode') ?? formMode.ADD));

    const [content, ] = useState(container.getAttribute('content') !== null ? parseInt(container.getAttribute('content')) : null);

    const [currentStep, setCurrentStep] = useState(parseInt(container.getAttribute('step') ?? initialStep));

    const gotoPrevStep = () => {
        setCurrentStep(1);
    }

    const props = { mode, content };

    const manageStep = () => {
        switch (currentStep) {
            case 1:
                return <Step1 {...props}/>;
            case 2:
                return <Step2 {...props}/>;
            default:
                return null;
        }
    }

    return (
        <React.Fragment>
            {manageStep()}
            <br/>
            <br/>
            <br/>
            {currentStep > 1 ?
                <button className="secondary button float-left" onClick={() => gotoPrevStep()}>Back</button>
            : null
            }
            {currentStep < 2 ?
                <button type="submit" className="secondary button float-right">Next</button>
            : null
            }
            {currentStep === 2 ?
                <button className="button float-right">
                    {mode === formMode.ADD ? 'Create' : 'Save Changes'}
                </button>
            : null
            }
        </React.Fragment>
    )
}