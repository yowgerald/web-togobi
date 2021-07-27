import React, { Component } from 'react';
import { Step1 } from './steps/Step1';
import { Step2 } from './steps/Step2';
import { formMode } from '../Constants';

export class ContentFormMaster extends Component {
    constructor(props) {
        super(props);

        let container = document.getElementById('root');
        this.state = {
            mode: parseInt(container.getAttribute('mode')),
            content: parseInt(container.getAttribute('content')),
            currentStep: parseInt(container.getAttribute('step'))
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

    componentDidMount() {
        if (this.state.mode === formMode.ADD) {
            this.setState({
                currentStep: 1
            });
        }
    }

    render() {
        return (
            <React.Fragment>
                <Step1 currentStep={this.state.currentStep} mode={this.state.mode} content={this.state.content}/>
                <Step2 currentStep={this.state.currentStep} mode={this.state.mode} content={this.state.content}/>
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