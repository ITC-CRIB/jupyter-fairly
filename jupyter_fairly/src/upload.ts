import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  InputDialog,
  Dialog
  Notification
} from '@jupyterlab/apputils';

import { 
  IFileBrowserFactory 
} from '@jupyterlab/filebrowser';

import { PromiseDelegate, ReadonlyJSONValue } from '@lumino/coreutils';

// Icons
import {
  fileUploadIcon,
} from '@jupyterlab/ui-components';
import { requestAPI } from './handler';
import { showErrorMessage } from '@jupyterlab/apputils';

/**
 * Uploads metadata and files to data repository
 */


 function uploadDataset(directory: string,  repository: string) {
  /**
   * upload local dataset to data reposotory
   * @param directory - realtive path to directory of local dataset
   * @param repository - name of data repository
   */

  /* ./ is necessary becaucause defaultBrowser.Model.path
  * returns an empty string when fileBlowser is on the
  * jupyterlab root directory     
  */
  let rootPath = './';

  var client;
  
  if(repository === '4TU.ResearchData') {
    client = '4tu';
  }
  else if (repository === 'Zenodo'){
    client = 'zenodo'
  }
  else if (repository === 'Figshare'){
    client = 'figshare'
  };

  let payload = JSON.stringify({
    directory: rootPath.concat(directory),  // TODO: this might not work in Windows
    client: client
  });

  // notification
  const delegate = new PromiseDelegate<ReadonlyJSONValue>();
  const complete = "complete";
  const failed = "failed"
  
  requestAPI<any>('upload', {
    method: 'POST', 
    body: payload
  }) 
  .then(data => {
    console.log(data);
    delegate.resolve({ complete });
  })
  .catch(reason => {
    delegate.reject({ failed });
    // show error when 
    showErrorMessage("Error when uploading dataset", reason)
  });

  Notification.promise(delegate.promise, {
    pending: { message: 'Uploading dataset...', options: { autoClose: false } },
    success: {
      message: (result: any) =>
      `Dataset upload ${result.complete}.`,
      options: {autoClose: 3000}
    },
    error: {message: () => `Upload failed.`}
  });

};


function pushDataset(localDataset: string) {
  /**
   * upload local dataset to data reposotory
   * @param localDataset - realtive path to directory of local dataset with remote metadata
   */

  /* ./ is necessary becaucause defaultBrowser.Model.path
  * returns an empty string when fileBlowser is on the
  * jupyterlab root directory     
  */
  let rootPath = './';

  let payload = JSON.stringify({
    localdataset: rootPath.concat(localDataset)
  });

  // notification
  const delegate = new PromiseDelegate<ReadonlyJSONValue>();
  const complete = "complete";
  const failed = "failed"
  
  requestAPI<any>('push', {
    method: 'PATCH', 
    body: payload
  }) 
  .then(data => {
    console.log(data);
    delegate.resolve({ complete });
  })
  .catch(reason => {
    delegate.reject({ failed });
    // show error when 
    showErrorMessage("Error when updating remote dataset", reason)
  });

  Notification.promise(delegate.promise, {
    pending: { message: 'Pushing dataset to repository ...', options: { autoClose: false } },
    success: {
      message: (result: any) =>
      `Remote dataset update ${result.complete}.`,
      options: {autoClose: 3000}
    },
    error: {message: () => `Pushing has failed.`}
  });

};


export const uploadDatasetPlugin: JupyterFrontEndPlugin<void> = {
  id: '@jupyter-fairly/upload',
  requires: [IFileBrowserFactory],
  autoStart: true,
  activate: (
    app: JupyterFrontEnd,
    fileBrowserFactory: IFileBrowserFactory
  ) => {
    console.log("uploadDatasetPlugin activated!!");
    // const fileBrowser = fileBrowserFactory.defaultBrowser;
    const fileBrowser = fileBrowserFactory.tracker.currentWidget;
    const fileBrowserModel = fileBrowser.model;

    
    const uploadDatasetCommand = "uploadDataset"
    app.commands.addCommand(uploadDatasetCommand, {
      label: 'Upload Dataset',
      isEnabled: () => true,
      isVisible: () => true, // activate only when current directory contains a manifest.yalm
      icon: fileUploadIcon,
      execute: async() => {

        // return relative path w.r.t. jupyterlab root path.
        // root-path = empty string.

        let targetRepository = await InputDialog.getItem({
          title: 'Select Data Repository',
          items: ['4TU.ResearchData',  'Zenodo', 'Figshare'],
          okLabel: 'Continue',
        });
        
        // initialize dataset when accept button is clicked and 
        // vaule for teamplate is not null
        if (targetRepository.button.accept && targetRepository.value) {
          
          let confirmAction = await InputDialog.getBoolean({
            title: 'Do you want to upload the dataset?',
            label: `Yes, upload metadata and files to ${targetRepository.value}`
          });

          if (confirmAction.button.accept){
            console.log ('uploading dataset');
            uploadDataset(fileBrowserModel.path, targetRepository.value)
          }else {
            console.log('do not archive');
            return
          };

        } else{
          console.log('rejected')
          return
        }

      }
    });


    const pushCommand = "pushDataset"
    app.commands.addCommand(pushCommand, {
      label: 'Push',
      isEnabled: () => true,
      isVisible: () => true, // activate only when current directory contains a manifest.yalm
      icon: fileUploadIcon,
      execute: async() => {

        // return relative path w.r.t. jupyterlab root path.
        // root-path = empty string.

        // Choose a better dialog for this
        let confirmAction = await InputDialog.getBoolean({
          title: 'Confirm the operation',
          label: `Yes, push changes to the data dataset`,
          okLabel: 'Push',
        });

        

        if (confirmAction.button.accept){
          console.log ('pushing changes to data repository');
          pushDataset(fileBrowserModel.path)
        }else {
          console.log('rejected');
          return
        };

      }
    });

    app.contextMenu.addItem({
      command: uploadDatasetCommand,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 104
    }
    );
    app.contextMenu.addItem({
      command: pushCommand,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 105
    }
    );
  }
};
