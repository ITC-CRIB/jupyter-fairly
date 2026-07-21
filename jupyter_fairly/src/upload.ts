import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  InputDialog,
  Notification,
  showDialog,
  Dialog
} from '@jupyterlab/apputils';

import { IDefaultFileBrowser } from '@jupyterlab/filebrowser';

import { PromiseDelegate, ReadonlyJSONValue } from '@lumino/coreutils';

import { PathExt } from '@jupyterlab/coreutils';

// Icons
import { fileUploadIcon, redoIcon } from '@jupyterlab/ui-components';
import { requestAPI } from './handler';
import { showErrorMessage } from '@jupyterlab/apputils';

function uploadDataset(directory: string, repository: string) {
  /**
   * upload local dataset to data reposotory
   * @param directory - realtive path to directory of local dataset
   * @param repository - name of data repository
   */

  /* file browser paths always use forward slashes and are empty
   * at the jupyterlab root directory; joining with '.' yields a
   * relative path the server can resolve on any OS ('.' at the root)
   */
  const directoryPath = PathExt.join('.', directory);

  let client: any;

  if (repository === '4TU.ResearchData') {
    client = '4tu';
  } else if (repository === 'Zenodo') {
    client = 'zenodo';
  } else if (repository === 'Figshare') {
    client = 'figshare';
  }

  const payload = JSON.stringify({
    directory: directoryPath,
    client: client
  });

  // notification
  const delegate = new PromiseDelegate<ReadonlyJSONValue>();
  const complete = 'complete';
  const failed = 'failed';

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
      showErrorMessage('Error when uploading dataset', reason);
    });

  Notification.promise(delegate.promise, {
    pending: { message: 'Uploading dataset...', options: { autoClose: false } },
    success: {
      message: (result: any) => `Dataset upload ${result.complete}.`,
      options: { autoClose: 3000 }
    },
    error: { message: () => `Upload failed.` }
  });
}

function pushDataset(localDataset: string) {
  /**
   * upload local dataset to data reposotory
   * @param localDataset - realtive path to directory of local dataset with remote metadata
   */

  /* file browser paths always use forward slashes and are empty
   * at the jupyterlab root directory; joining with '.' yields a
   * relative path the server can resolve on any OS ('.' at the root)
   */
  const payload = JSON.stringify({
    localdataset: PathExt.join('.', localDataset)
  });

  // notification
  const delegate = new PromiseDelegate<ReadonlyJSONValue>();
  const complete = 'complete';
  const failed = 'failed';

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
      showErrorMessage('Error when updating remote dataset', reason);
    });

  Notification.promise(delegate.promise, {
    pending: {
      message: 'Pushing dataset to repository ...',
      options: { autoClose: false }
    },
    success: {
      message: (result: any) => `Remote dataset update ${result.complete}.`,
      options: { autoClose: 3000 }
    },
    error: { message: () => `Pushing has failed.` }
  });
}

export const uploadDatasetPlugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyter-fairly:upload',
  description: 'Upload dataset plugin',
  requires: [IDefaultFileBrowser],
  autoStart: true,
  activate: (app: JupyterFrontEnd, defaultFileBrowser: IDefaultFileBrowser) => {
    console.log('uploadDatasetPlugin activated!!');
    const fileBrowserModel = defaultFileBrowser.model;

    // ** Upload a new dataset to a data repository **
    const uploadDatasetCommand = 'uploadDataset';
    app.commands.addCommand(uploadDatasetCommand, {
      label: 'Upload Dataset',
      isEnabled: () => true,
      isVisible: () => true, // activate only when current directory contains a manifest.yalm
      icon: fileUploadIcon,
      execute: async () => {
        // return relative path w.r.t. jupyterlab root path.
        // root-path = empty string.

        const targetRepository = await InputDialog.getItem({
          title: 'Select Data Repository',
          items: ['4TU.ResearchData', 'Zenodo', 'Figshare'],
          okLabel: 'Continue'
        });

        // initialize dataset when accept button is clicked and
        // vaule for teamplate is not null
        if (targetRepository.button.accept && targetRepository.value) {
          const confirmAction = await InputDialog.getBoolean({
            title: 'Do you want to upload the dataset?',
            label: `Yes, upload metadata and files to ${targetRepository.value}`
          });

          if (confirmAction.button.accept) {
            console.log('uploading dataset');
            uploadDataset(fileBrowserModel.path, targetRepository.value);
          } else {
            console.log('do not archive');
            return;
          }
        } else {
          console.log('rejected');
          return;
        }
      }
    });

    // ** Push changes made to a local dataset to a data repository **
    const pushCommand = 'pushDataset';
    app.commands.addCommand(pushCommand, {
      label: 'Push',
      isEnabled: () => true,
      isVisible: () => true, // activate only when current directory contains a manifest.yalm
      icon: redoIcon,
      execute: async () => {
        const confirmAction = await showDialog({
          title: 'Push changes', // Can be text or a react element
          body: 'This will update the data repository using changes made here.',
          host: document.body, // Parent element for rendering the dialog
          buttons: [Dialog.cancelButton(), Dialog.okButton({ label: 'Push' })]
        });

        if (confirmAction.button.accept) {
          await pushDataset(fileBrowserModel.path);
        } else {
          console.log('rejected');
          return;
        }
      }
    });

    app.contextMenu.addItem({
      command: uploadDatasetCommand,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 104
    });
    app.contextMenu.addItem({
      command: pushCommand,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 105
    });
  }
};
