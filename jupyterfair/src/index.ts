import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ICommandPalette,} from '@jupyterlab/apputils';

import { 
  createDatasetCommandPlugin,
  cloneDatasetCommandPlugin, 
} from './dataset';
import {editMetadataPlugin} from './metadata'
import { archiveDatasetPlugin} from './archive';

// import { FairlyWidget } from './widgets/FairlyTab';


/**
 *  Activate jupyterfair extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterfair:plugin',
  autoStart: true,
  requires : [ICommandPalette],
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd,
    palette: ICommandPalette, 
    settingRegistry: ISettingRegistry | null) => {
    
      console.log('jupytefair is activated!!');
      
      // this doesn't do what is expected
      // See: https://stackoverflow.com/questions/63065310/how-do-i-create-a-jupyter-lab-extension-that-adds-a-custom-button-to-the-toolba
      const openFairlyTabCommand = 'widgets:open-tab';
      app.commands.addCommand( openFairlyTabCommand, {
        label: 'Open Fairly Tab',
        caption: 'Open the Fairly Tab',
        // isEnabled: () => true,
        // isVisible: () => true,
        execute: () => {
          // const widget = new FairlyWidget();
          // app.shell.add(widget, 'main');
        }
      });
      palette.addItem({command: openFairlyTabCommand, category: 'Fairly'});
  }
};
















export default [
  plugin, 
  createDatasetCommandPlugin, 
  editMetadataPlugin, 
  archiveDatasetPlugin,
  cloneDatasetCommandPlugin
];

//Todo: add new tab to left pannel
// example: https://github.com/jupyterlab/extension-examples/tree/master/widgets
