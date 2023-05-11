
import { 
  JupyterFrontEnd, 
  JupyterFrontEndPlugin } from '@jupyterlab/application';
import { 
  ICommandPalette,
  // WidgetTracker 
 } from '@jupyterlab/apputils';

import {
  Menu
} from '@lumino/widgets';

export const FairlyMenuPlugin: JupyterFrontEndPlugin<void> = {  
  id: 'jupyter-fairly-menu:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd, palette: ICommandPalette) => {
    console.log('main menu is activated!!');

    // Create a new command
    const commandId = 'fairlymenucommand';
    app.commands.addCommand(commandId, {
      label: 'my command',
      execute: () => {
        console.log('my command is executed');
      }
    });

    // Add the command to the palette.
    palette.addItem({ command: commandId, category: 'Fairly' });

    // Create a menu
    const menu = new Menu({ commands: app.commands });
    menu.title.label = 'Fairly Menu';

    // Add some commands to the menu  
    menu.addItem({ command: commandId });

    // Add the menu to the main menu
    app.shell.add(menu, 'Edit');
  }
};