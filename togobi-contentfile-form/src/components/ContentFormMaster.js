import React, { Component } from 'react';
import { Step1 } from './steps/Step1';
import { Step2 } from './steps/Step2';
import { formMode } from '../Constants';

export class ContentFormMaster extends Component {
    constructor(props) {
        super(props);

        let container = document.getElementById('root');
        this.state = {
            mode: parseInt(container.getAttribute('mode') ?? formMode.ADD),
            content: container.getAttribute('content') !== null ? parseInt(container.getAttribute('content')) : null,
            currentStep: parseInt(container.getAttribute('step') ?? 1)
        }
    }

    gotoToNextStep() {
        // TODO: save content, then update content state from response
    }

    gotoPrevStep() {
        this.setState({
            currentStep: 1
        });
    }

    saveContent() {
        // TODO: final saving
    }

    manageStep() {
        switch(this.state.currentStep) {
            case 1:
                return <Step1 currentStep={this.state.currentStep} mode={this.state.mode} content={this.state.content}/>;
            case 2:
                return <Step2 currentStep={this.state.currentStep} mode={this.state.mode} content={this.state.content}/>;
            default:
                return null;
        }
    }

    render() {
        return (
            <React.Fragment>
                {this.manageStep()}

                {this.state.currentStep > 1 ?
                    <button className='secondary button float-left' onClick={() => this.gotoPrevStep()}>Back</button>
                : null
                }

                {this.state.currentStep < 2 ?
                    <button type='submit' className='secondary button float-right'>Next</button>
                : null
                }

                {this.state.currentStep === 2 ?
                    <button className='button float-right' onClick={() => this.saveContent()}>
                        {this.state.mode === formMode.ADD ? 'Create' : 'Save Changes'}
                    </button>
                : null
                }
            </React.Fragment>
        )
    }
}