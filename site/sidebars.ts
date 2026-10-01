import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

/**
 * Manual flat sidebar.
 *
 * Every entry is a single clickable link to a Level 2 overview page.
 * No categories, no expansion, no nested children. Sub-pages (Level 3+)
 * are reached by navigating into the corresponding overview page.
 *
 * Order matches the `position` values previously set in each top-level
 * `_category_.json` file. New Level 2 sections should be added here in
 * the appropriate slot.
 */
const sidebars: SidebarsConfig = {
  docs: [
    {type: 'doc', id: 'charlie-kirk', label: 'Home'},
    {type: 'doc', id: 'Mic/overview', label: 'Microphone'},
    {type: 'doc', id: 'court/overview', label: 'Court & Trial'},
    {type: 'doc', id: 'Cause_of_Death/overview', label: 'Cause of Death'},
    {type: 'doc', id: 'Amfest/overview', label: 'AmFest'},
    {type: 'doc', id: 'Fix/overview', label: 'Charlie Kirk Laws'},
    {type: 'doc', id: 'Timeline/overview', label: 'Timeline'},
    {type: 'doc', id: 'maps/overview', label: 'Maps'},
    {type: 'doc', id: 'UVU/overview', label: 'UVU Campus'},
    {type: 'doc', id: 'Consciousness_Control/overview', label: 'Mind Control (Tyler?)'},
    {type: 'doc', id: 'Your_Actions_Fix_It/overview', label: 'Your Actions Fix It'},
    {type: 'doc', id: 'Media/overview', label: 'Media'},
    {type: 'doc', id: 'GoogleSearches/overview', label: 'Google Searches'},
    {type: 'doc', id: 'Legal/overview', label: 'Legal'},
    {type: 'doc', id: 'Topics', label: 'Investigation Topics'},
  ],
};

export default sidebars;
