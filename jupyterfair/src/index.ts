import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { ICommandPalette,} from '@jupyterlab/apputils';

// import { Widget } from '@lumino/widgets';

// import handlers from Jupyter Server extension
// import { requestAPI } from './handler';

/**
 * Initialization data for the jupyterfair extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterfair:plugin',
  autoStart: true,
  requires : [ICommandPalette],
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette, settingRegistry: ISettingRegistry | null) => {
    console.log('JupyterLab extension jupyterfair widget is activated! 07-11');
    // console.log('IcommandPalette:', palette);
    
    // Declare command
    const commandCreateDataset = 'Create Dataset';
    let toggled = false;

    // add command to registry
    app.commands.addCommand(commandCreateDataset, {
      label: 'Create Dataset...',
      isEnabled: () => true,
      isVisible: () => true,
      isToggled: () => toggled,
      execute: () => {
        console.log(`Executed ${commandCreateDataset}`);
        toggled = !toggled;
      }
    });

    // append command to GUI elements
    // Ex. To command palette
    palette.addItem({
      command: commandCreateDataset,
      category: 'Fairly',
      args: {} 
    });

    // ex. To context menu
    app.contextMenu.addItem({
      command: commandCreateDataset,
      selector: '.jp-DirListing-item[data-isdir="false"]',
      rank: 100
    });

    // for examples: https://discourse.jupyter.org/t/add-entries-to-the-filebrowser-contextmenu/1651/2
  
  }
};

export default plugin;
