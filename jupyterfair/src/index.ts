import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { ICommandPalette, MainAreaWidget } from '@jupyterlab/apputils';

import { Widget } from '@lumino/widgets';

// import handlers from Jupyter Server extension
import { requestAPI } from './handler';

/**
 * Initialization data for the jupyterfair extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterfair:plugin',
  autoStart: true,
  requires : [ICommandPalette],
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette, settingRegistry: ISettingRegistry | null) => {
    console.log('JupyterLab extension jupyterfair is activated!');
    console.log('ICommandPalette:', palette);

    //Add command example
    const {commands} = app;

    const command = 'jlab-examples:command';

    // add command
    commands.addCommand(command, {
      label: 'Execute jlab-examples:command Command',
      caption: 'Execute jlab-examples:command Command',
      execute: (args: any) => {
        const orig = args['origin'];
        console.log(`jlab-examples:command has been called from ${orig}.`);
        if (orig !== 'init') {
          window.alert(`jlab-examples:command has been called from ${orig}.`);
        }
      },
    });

    //call command execution
    commands.execute(command, {origin: 'init'}).catch((reason) => {
      console.error(
        `An error occurred during the execution of jlab:examples:command.\n${reason}.`
      );
    });
    
    // End of add command example

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('jupyterfair settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for jupyterfair.', reason);
        });
    }

    requestAPI<any>('datasets')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The jupyterfair server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
