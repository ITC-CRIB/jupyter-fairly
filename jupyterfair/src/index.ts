import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import {
  // Dialog, 
  ICommandPalette, 
  // showDialog,
  InputDialog,
  // showErrorMessage,

} from '@jupyterlab/apputils';
import {
  IFileBrowserFactory,
  // FileBrowser,
  // FilterFileBrowserModel,
  
} from '@jupyterlab/filebrowser';

// import { DocumentManager } from '@jupyterlab/docmanager';

// import { DocumentRegistry } from '@jupyterlab/docregistry';

import {pathCommandPlugin} from './index-copy'

// Icons
import {
  addIcon,
  editIcon,
  fileUploadIcon,
  // textEditorIcon,
  // closeIcon,
  // copyIcon,
  // cutIcon,
  // downloadIcon,
  // editIcon,
  // fileIcon,
  // folderIcon,
  // linkIcon,
  // markdownIcon,
  // newFolderIcon,
  // pasteIcon,
  // RankedMenu,
  // refreshIcon,
  // stopIcon,
  // textEditorIcon
} from '@jupyterlab/ui-components'

// import { showDialog} from '@jupyterlab/apputils';
// import { Dialog} from '@jupyterlab/apputils';
//examples with Dialog widget: https://www.programcreek.com/typescript/?api=@jupyterlab/apputils.Dialog


// import handlers from Jupyter Server extension
import { 
  initDataset 
} from './fairly-api';



/**
 * Initialization data for the jupyterfair extension.
 */
const newDataset: JupyterFrontEndPlugin<void> = {
  id: 'jupyterfair:newDataset',
  autoStart: true,
  requires : [ICommandPalette, IFileBrowserFactory],
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, factory: IFileBrowserFactory, palette: ICommandPalette, settingRegistry: ISettingRegistry | null) => {
    console.log('JupyterLab extension jupyterfair widget is activated! 07-11');
    // console.log('IcommandPalette:', palette);

    // Declare command
    const commandCreateDataset = 'fairly:create';
   
    // add command to registry
    app.commands.addCommand(commandCreateDataset, {
      label: 'Create Fairly Dataset',
      isEnabled: () => true,
      isVisible: () => true,
      icon: addIcon,
      execute: async () => {
        console.log(`Executed ${commandCreateDataset}`);
    
        let metadataTemplate = await InputDialog.getItem({
          title: 'Select format for new dataset\'s metadata',
          items: ['', 'Default', '4TU.Research',  'Zenodo', 'Figshare'],
          okLabel: 'Create',
        });
        
        // initialize dataset when accept button is clicked and 
        // vaule for teamplate is not null
        if (metadataTemplate.button.accept && metadataTemplate.value) {
          let root_path = './'
          initDataset(root_path , metadataTemplate.value);
        } else{
          console.log('rejected')
          return
        }
      }
    });
  
    // Add to context menu
      // for examples: https://discourse.jupyter.org/t/add-entries-to-the-filebrowser-contextmenu/1651/2
    app.contextMenu.addItem({
      command: commandCreateDataset,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 100
    });

    const commandEditMetadata = 'fairly:edit-metadata'
    // Opens the manifest.yalm file in the file editor
    app.commands.addCommand(commandEditMetadata, {
      label: 'Edit Dataset Metadata',
      isEnabled: () => true,
      isVisible: () => true,
      icon: editIcon,
      execute: async () => {
        console.log(`Executed ${commandEditMetadata}`);
        

        if (true) {
          console.log('accepted');
        } else{
          console.log('rejected')
        }
      }
    });


    app.contextMenu.addItem({
      command: commandEditMetadata,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 101
    });

    const commandArchiveDataset = 'fairly:archive'
    // Archives dataset to selected Data repository
    app.commands.addCommand(commandArchiveDataset, {
      label: 'Archive Dataset',
      isEnabled: () => true,
      isVisible: () => true,
      icon: fileUploadIcon,
      execute: async () => {
        console.log(`Executed ${commandArchiveDataset}`);

        let targetRepository = await InputDialog.getItem({
          title: 'Select Data Repository',
          items: ['4TU.ResearchData',  'Zenodo', 'Figshare'],
          okLabel: 'Continue',
        });
        
        // initialize dataset when accept button is clicked and 
        // vaule for teamplate is not null
        if (targetRepository.button.accept && targetRepository.value) {
          
          let confirmAction = await InputDialog.getBoolean({
            title: 'Do you want to archive the dataset?',
            label: `Yes, upload metadata and files to ${targetRepository.value}`
          });

          if (confirmAction.button.accept){
            console.log ('archive dataset');
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

    app.contextMenu.addItem({
      command: commandArchiveDataset,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 102
    });

  // Clone an existing dataset to current directory
  // based on url, iod(url)
  const commandCloneDataset = 'fairly:clone';
  app.contextMenu.addItem({
    command: commandCloneDataset,
    // matches anywhere in the filebrowser
    selector: '.jp-DirListing-content',
    rank: 103
  });
  
  }
};

export default [newDataset, pathCommandPlugin];
