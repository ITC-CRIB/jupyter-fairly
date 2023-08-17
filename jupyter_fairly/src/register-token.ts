import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  InputDialog
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

/**
 * Registers a token to the fairly configuration file at ~/.fairly/config.json
 */


 function registerToken(repository: string,  token: string) {
  /**
   * register token to fairly configuration file
   * @param repository- name of data repository
   * @param token - access token for data repository
   */

  var repositoryId;
  
  if(repository === '4TU.ResearchData') {
    repositoryId = '4tu';
  }
  else if (repository === 'Zenodo'){
    repositoryId = 'zenodo'
  }
  else if (repository === 'Figshare'){
    repositoryId = 'figshare'
  };

  let payload = JSON.stringify({
    repository: repositoryId,  
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


export const registerTokenPlugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyter-fairly:register-token',
  requires: [IFileBrowserFactory],
  autoStart: true,
  activate: (
    app: JupyterFrontEnd,
  ) => {
    console.log("registerTokenPlugin activated!!");

    const registerTokenCommand = 'registerAccessToken'
    app.commands.addCommand(registerTokenCommand, {
      label: 'Register Token',
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

    app.contextMenu.addItem({
      command: registerTokenCommand,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 102
    });
  }
};
