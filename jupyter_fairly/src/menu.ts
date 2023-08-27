import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import {
    InputDialog,
    // ICommandPalette,
  } from '@jupyterlab/apputils';
  
  import { 
    IFileBrowserFactory 
  } from '@jupyterlab/filebrowser';
  
  // Icons
  import {
    settingsIcon,
  } from '@jupyterlab/ui-components';
  import { requestAPI } from './handler';
  import { showErrorMessage } from '@jupyterlab/apputils';
  

  function registerToken(repository: string,  token: string) {
    /**
     * register token to fairly configuration file
     * @param repository- name of data repository
     * @param token - access token for data repository
     */
  
    var clientId;
    
    if(repository === '4TU.ResearchData') {
      clientId = '4tu';
    }
    else if (repository === 'Zenodo'){
      clientId = 'zenodo'
    }
    else if (repository === 'Figshare'){
      clientId = 'figshare'
    };
  
    let payload = JSON.stringify({
      client: clientId,  
      token: token
    });
  
    console.log(payload);
    
    requestAPI<any>('repo-token', {
      method: 'POST', 
      body: payload
    }) 
    .then(data => {
      console.log(data);
    })
    .catch(reason => {
      // show error when requestAPI fails
      showErrorMessage("Error when registering access token", reason)
    });
  };


/**
 * Initialization data for the main menu example.
 */
export const FairlyMenuPlugin: JupyterFrontEndPlugin<void> = {
    id: '@jupyter-fairly/mainmenu',
    requires: [IFileBrowserFactory],
  autoStart: true,
  activate: (
    app: JupyterFrontEnd,
  ) => {
    console.log("registerTokenPlugin activated!!");

    const registerTokenCommand = 'registerAccessToken'
    app.commands.addCommand(registerTokenCommand, {
      label: 'Add Repository Token',
      isEnabled: () => true,
      isVisible: () => true, 
      icon: settingsIcon,
      execute: async() => {

        // Asks for the data repository
        let targetRepository = await InputDialog.getItem({
          title: 'Register Access Token. Select Data Repository',
          items: ['4TU.ResearchData', 'Zenodo', 'Figshare'],
          okLabel: 'Continue',
        });
        
        if (targetRepository.button.accept && targetRepository.value) {
          
          // Asks for the access token
          let accessToken = await InputDialog.getText({
            title: 'Enter Access Token for: '.concat(targetRepository.value),
            placeholder: 'Access Token',
            okLabel: 'Add Token',
          });

          if (accessToken.button.accept){
            console.log ('registeing token');
            registerToken(targetRepository.value, accessToken.value)
          }else {
            console.log('operation was canceled by the user');
            return
          };

        } else{
          console.log('canceled')
          return
        };
      }
    });

    const openURLCommand = 'fairly:openURL'
    app.commands.addCommand(openURLCommand, {
      label: 'Fairly Documentation',
      caption: 'Fairly Documentation',
      execute: (args: any) => {
        window.open(`${args['url']}`, '_blank');      
      }
    });  
  }
}
