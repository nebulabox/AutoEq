# -*- coding: utf-8 -*-

import sys
import json
import re
from pathlib import Path
from tqdm.auto import tqdm
from autoeq.constants import SAMPLE_REGEX
from autoeq.frequency_response import FrequencyResponse
ROOT_PATH = Path(__file__).parent.parent
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(1, str(ROOT_PATH))
from dbtools.constants import WEBAPP_PATH, MEASUREMENTS_PATH, TARGETS_PATH


def measurement_rank(entry):
    order = [
        {'source': 'nebulabox', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'nebulabox', 'form': 'over-ear', 'rig': 'unknown'},
        
        {'source': 'oratory1990', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'crinacle', 'form': 'over-ear', 'rig': 'GRAS 43AG-7'},
        {'source': 'innerfidelity', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'rtings', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'headphonecom', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'crinacle', 'form': 'over-ear', 'rig': 'EARS + 711'},

        {'source': 'crinacle', 'form': 'in-ear', 'rig': 'Bruel & Kjaer 4620'},
        {'source': 'oratory1990', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'crinacle', 'form': 'in-ear', 'rig': '711'},
        {'source': 'rtings', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'innerfidelity', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'headphonecom', 'form': 'in-ear', 'rig': 'unknown'},

        {'source': 'oratory1990', 'form': 'earbud', 'rig': 'unknown'},
        {'source': 'crinacle', 'form': 'earbud', 'rig': '711'},
        {'source': 'rtings', 'form': 'earbud', 'rig': 'unknown'},
        {'source': 'innerfidelity', 'form': 'earbud', 'rig': 'unknown'},
        {'source': 'headphonecom', 'form': 'earbud', 'rig': 'unknown'},
        {'source': 'HypetheSonics', 'form': 'in-ear', 'rig': 'GRAS RA0045'},
        {'source': 'Innerfidelity', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Regan Cipher', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Innerfidelity', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'Rtings', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'HypetheSonics', 'form': 'in-ear', 'rig': 'Bruel & Kjaer 5128'},
        {'source': 'freeryder05', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Super Review', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Harpo', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Kazi', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'ToneDeafMonk', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Jaytiss', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'RikudouGoku', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Fahryst', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Hi End Portable', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': "Ted's Squig Hoard", 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'kr0mka', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Auriculares Argentina', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Rtings', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'Headphone.com Legacy', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'Headphone.com Legacy', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Kuulokenurkka', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'Filk', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'Super Review', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'Auriculares Argentina', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'kr0mka', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'Rtings', 'form': 'earbud', 'rig': 'unknown'},
        {'source': 'Regan Cipher', 'form': 'earbud', 'rig': 'unknown'},
        {'source': 'DHRME', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Super Review', 'form': 'earbud', 'rig': 'unknown'},
        {'source': 'Innerfidelity', 'form': 'earbud', 'rig': 'unknown'},
        {'source': 'Headphone.com Legacy', 'form': 'earbud', 'rig': 'unknown'},
        {'source': 'HypetheSonics', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'Bakkwatan', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Regan Cipher', 'form': 'over-ear', 'rig': 'unknown'},
        {'source': 'HypetheSonics', 'form': 'earbud', 'rig': 'unknown'},
        {'source': 'kr0mka', 'form': 'earbud', 'rig': 'unknown'},
        {'source': 'Filk', 'form': 'in-ear', 'rig': 'unknown'},
        {'source': 'Kazi', 'form': 'earbud', 'rig': 'unknown'} ,
        {'source': 'rtings', 'form': 'in-ear', 'rig': 'HMS II.3'},
        {'source': 'rtings', 'form': 'over-ear', 'rig': 'HMS II.3'},
        {'source': 'rtings', 'form': 'earbud', 'rig': 'HMS II.3'},
        {'source': 'rtings', 'form': 'over-ear', 'rig': 'Bruel & Kjaer 5128'},
        {'source': 'rtings', 'form': 'in-ear', 'rig': 'Bruel & Kjaer 5128'},
        {'source': 'rtings', 'form': 'earbud', 'rig': 'Bruel & Kjaer 5128'},
        {'source': 'Rtings', 'form': 'over-ear', 'rig': 'HMS II.3'},
        {'source': 'Rtings', 'form': 'earbud', 'rig': 'HMS II.3'},
        {'source': 'Rtings', 'form': 'in-ear', 'rig': 'HMS II.3'},
        {'source': 'Rtings', 'form': 'over-ear', 'rig': 'Bruel & Kjaer 5128'},
        {'source': 'Rtings', 'form': 'in-ear', 'rig': 'Bruel & Kjaer 5128'},
        {'source': 'Rtings', 'form': 'earbud', 'rig': 'Bruel & Kjaer 5128'},
        {'source': 'DHRME', 'form': 'over-ear', 'rig': 'unknown'},
    ]
    return order.index({'source': entry['source'], 'form': entry['form'], 'rig': entry['rig']})


def write_entries_and_measurements():
    entries = dict()
    measurements = dict()
    files = sorted(MEASUREMENTS_PATH.glob('**/data/**/*.csv'), key=lambda x: x.name)
    for hp_path in tqdm(files):
        parts = hp_path.parts[hp_path.parts.index('data') + 1:]
        source = hp_path.parts[hp_path.parts.index('data') - 1]
        form = parts[0]
        rig = parts[1] if len(parts) == 3 else 'unknown'
        if source == 'crinacle' and rig == 'unknown':
            print(parts)
            print(hp_path)
            return
        name = parts[-1].replace('.csv', '')
        if SAMPLE_REGEX.search(name):
            # Skip individual samples
            continue
        if name not in entries:
            entries[name] = []
        if name not in measurements:
            measurements[name] = dict()
        if source not in measurements[name]:
            measurements[name][source] = dict()
        measurements[name][source][rig] = FrequencyResponse.read_csv(hp_path).to_dict()
        entries[name].append({
            'form': form, 'rig': rig, 'source': source
        })
    entries = {key: entries[key] for key in sorted(list(entries.keys()), key=lambda key: key)}
    for headphone in entries.keys():
        entries[headphone] = sorted(entries[headphone], key=lambda entry: measurement_rank(entry))
    with open(WEBAPP_PATH.joinpath('data', 'measurements.json'), 'w', encoding='utf-8') as fh:
        json.dump(measurements, fh, ensure_ascii=False, indent=4)
    with open(WEBAPP_PATH.joinpath('data', 'entries.json'), 'w', encoding='utf-8') as fh:
        json.dump(entries, fh, ensure_ascii=False, indent=4)


def write_targets():
    ####### [BEGIN] standard from dbtools ########
    targets = [
        {
            'file': TARGETS_PATH.joinpath('AutoEq in-ear.csv'),
            'compatible': [
                {'source': 'nebulabox', 'form': 'in-ear'},
                {'source': 'Auriculares Argentina', 'form': 'in-ear'},
                {'source': 'Bakkwatan', 'form': 'in-ear'},
                {'source': 'crinacle', 'form': 'in-ear', 'rig': '711'},
                {'source': 'DHRME', 'form': 'in-ear'},
                {'source': 'Fahryst', 'form': 'in-ear'},
                {'source': 'Filk', 'form': 'in-ear'},
                {'source': 'freeryder05', 'form': 'in-ear'},
                {'source': 'Harpo', 'form': 'in-ear'},
                {'source': 'Hi End Portable', 'form': 'in-ear'},
                {'source': 'HypetheSonics', 'form': 'in-ear', 'rig': 'GRAS RA0045'},
                {'source': 'Jaytiss', 'form': 'in-ear'},
                {'source': 'Kazi', 'form': 'in-ear'},
                {'source': 'Kazi', 'form': 'earbud'},
                {'source': 'kr0mka', 'form': 'in-ear'},
                {'source': 'kr0mka', 'form': 'earbud'},
                {'source': 'oratory1990', 'form': 'in-ear'},
                {'source': 'oratory1990', 'form': 'earbud'},
                {'source': 'Regan Cipher', 'form': 'in-ear'},
                {'source': 'Regan Cipher', 'form': 'earbud'},
                {'source': 'RikudouGoku', 'form': 'in-ear'},
                {'source': 'Super Review', 'form': 'in-ear'},
                {'source': 'Super Review', 'form': 'earbud'},
                {'source': 'Ted\'s Squig Hoard', 'form': 'in-ear'},
                {'source': 'ToneDeafMonk', 'form': 'in-ear'},
            ],
            'recommended': [
                {'source': 'nebulabox', 'form': 'in-ear'},
                {'source': 'Auriculares Argentina', 'form': 'in-ear'},
                {'source': 'Bakkwatan', 'form': 'in-ear'},
                {'source': 'crinacle', 'form': 'in-ear', 'rig': '711'},
                {'source': 'DHRME', 'form': 'in-ear'},
                {'source': 'Fahryst', 'form': 'in-ear'},
                {'source': 'Filk', 'form': 'in-ear'},
                {'source': 'freeryder05', 'form': 'in-ear'},
                {'source': 'Harpo', 'form': 'in-ear'},
                {'source': 'Hi End Portable', 'form': 'in-ear'},
                {'source': 'HypetheSonics', 'form': 'in-ear', 'rig': 'GRAS RA0045'},
                {'source': 'Jaytiss', 'form': 'in-ear'},
                {'source': 'Kazi', 'form': 'in-ear'},
                {'source': 'Kazi', 'form': 'earbud'},
                {'source': 'kr0mka', 'form': 'in-ear'},
                {'source': 'kr0mka', 'form': 'earbud'},
                {'source': 'oratory1990', 'form': 'in-ear'},
                {'source': 'oratory1990', 'form': 'earbud'},
                {'source': 'Regan Cipher', 'form': 'in-ear'},
                {'source': 'Regan Cipher', 'form': 'earbud'},
                {'source': 'RikudouGoku', 'form': 'in-ear'},
                {'source': 'Super Review', 'form': 'in-ear'},
                {'source': 'Super Review', 'form': 'earbud'},
                {'source': 'Ted\'s Squig Hoard', 'form': 'in-ear'},
                {'source': 'ToneDeafMonk', 'form': 'in-ear'},
            ],
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 8}
        },
        {
            'file': TARGETS_PATH.joinpath('crinacle EARS + 711 Harman over-ear 2018 without bass.csv'),
            'label': 'crinacle EARS + 711 Harman over-ear 2018',
            'compatible': [
                {'source': 'crinacle', 'form': 'over-ear', 'rig': 'EARS + 711'},
            ],
            'recommended': [
                {'source': 'crinacle', 'form': 'over-ear', 'rig': 'EARS + 711'},
            ],
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 6}
        },
        {
            'file': TARGETS_PATH.joinpath('Diffuse field 5128 -1dB per octave.csv'),
            'label': 'Diffuse Field 5128 (-1 dB/oct)',
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 0}
        },
        {
            'file': TARGETS_PATH.joinpath('zero.csv'),
            'label': 'Flat',
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 0}
        },
        {
            'file': TARGETS_PATH.joinpath('Harman in-ear 2019 without bass.csv'),
            'label': 'Harman in-ear 2019',
            'compatible': [
                {'source': 'nebulabox', 'form': 'in-ear'},
                {'source': 'Auriculares Argentina', 'form': 'in-ear'},
                {'source': 'Bakkwatan', 'form': 'in-ear'},
                {'source': 'crinacle', 'form': 'in-ear', 'rig': '711'},
                {'source': 'DHRME', 'form': 'in-ear'},
                {'source': 'Fahryst', 'form': 'in-ear'},
                {'source': 'Filk', 'form': 'in-ear'},
                {'source': 'freeryder05', 'form': 'in-ear'},
                {'source': 'Harpo', 'form': 'in-ear'},
                {'source': 'Hi End Portable', 'form': 'in-ear'},
                {'source': 'HypetheSonics', 'form': 'in-ear', 'rig': 'GRAS RA0045'},
                {'source': 'Jaytiss', 'form': 'in-ear'},
                {'source': 'Kazi', 'form': 'in-ear'},
                {'source': 'Kazi', 'form': 'earbud'},
                {'source': 'kr0mka', 'form': 'in-ear'},
                {'source': 'oratory1990', 'form': 'in-ear'},
                {'source': 'oratory1990', 'form': 'earbud'},
                {'source': 'Regan Cipher', 'form': 'in-ear'},
                {'source': 'Regan Cipher', 'form': 'earbud'},
                {'source': 'RikudouGoku', 'form': 'in-ear'},
                {'source': 'Super Review', 'form': 'in-ear'},
                {'source': 'Super Review', 'form': 'earbud'},
                {'source': 'Ted\'s Squig Hoard', 'form': 'in-ear'},
                {'source': 'ToneDeafMonk', 'form': 'in-ear'},
            ],
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 9.5}
        },
        {
            'file': TARGETS_PATH.joinpath('Harman over-ear 2018 without bass.csv'),
            'label': 'Harman over-ear 2018',
            'compatible': [
                {'source': 'nebulabox', 'form': 'over-ear'},
                {'source': 'Auriculares Argentina', 'form': 'over-ear'},
                {'source': 'crinacle', 'form': 'over-ear', 'rig': 'GRAS 43AG-7'},
                {'source': 'Filk', 'form': 'over-ear'},
                {'source': 'kr0mka', 'form': 'over-ear'},
                {'source': 'Kuulokenurkka', 'form': 'over-ear'},
                {'source': 'oratory1990', 'form': 'over-ear'},
                {'source': 'Regan Cipher', 'form': 'over-ear'},
                {'source': 'RikudouGoku', 'form': 'over-ear'},
                {'source': 'Super Review', 'form': 'over-ear'},
            ],
            'recommended': [
                {'source': 'nebulabox', 'form': 'over-ear'},
                {'source': 'Auriculares Argentina', 'form': 'over-ear'},
                {'source': 'crinacle', 'form': 'over-ear', 'rig': 'GRAS 43AG-7'},
                {'source': 'Filk', 'form': 'over-ear'},
                {'source': 'kr0mka', 'form': 'over-ear'},
                {'source': 'Kuulokenurkka', 'form': 'over-ear'},
                {'source': 'oratory1990', 'form': 'over-ear'},
                {'source': 'Regan Cipher', 'form': 'over-ear'},
                {'source': 'RikudouGoku', 'form': 'over-ear'},
                {'source': 'Super Review', 'form': 'over-ear'},
            ],
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 6}
        },
        {
            'file': TARGETS_PATH.joinpath('HMS II.3 AutoEq in-ear.csv'),
            'compatible': [
                {'source': 'nebulabox', 'form': 'in-ear'},
                {'source': 'Headphone.com Legacy', 'form': 'in-ear'},
                {'source': 'Headphone.com Legacy', 'form': 'earbud'},
                {'source': 'Innerfidelity', 'form': 'in-ear'},
                {'source': 'Innerfidelity', 'form': 'earbud'},
                {'source': 'Rtings', 'form': 'in-ear', 'rig': 'HMS II.3'},
                {'source': 'Rtings', 'form': 'earbud', 'rig': 'HMS II.3'},
            ],
            'recommended': [
                {'source': 'Headphone.com Legacy', 'form': 'in-ear'},
                {'source': 'Headphone.com Legacy', 'form': 'earbud'},
                {'source': 'Innerfidelity', 'form': 'in-ear'},
                {'source': 'Innerfidelity', 'form': 'earbud'},
                {'source': 'Rtings', 'form': 'in-ear', 'rig': 'HMS II.3'},
                {'source': 'Rtings', 'form': 'earbud', 'rig': 'HMS II.3'},
            ],
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 8}
        },
        {
            'file': TARGETS_PATH.joinpath('HMS II.3 Harman in-ear 2019 without bass.csv'),
            'label': 'HMS II.3 Harman in-ear 2019',
            'compatible': [
                {'source': 'nebulabox', 'form': 'in-ear'},
                {'source': 'Headphone.com Legacy', 'form': 'in-ear'},
                {'source': 'Headphone.com Legacy', 'form': 'earbud'},
                {'source': 'Innerfidelity', 'form': 'in-ear'},
                {'source': 'Innerfidelity', 'form': 'earbud'},
                {'source': 'Rtings', 'form': 'in-ear', 'rig': 'HMS II.3'},
                {'source': 'Rtings', 'form': 'earbud', 'rig': 'HMS II.3'},
            ],
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 9.5}
        },
        {
            'file': TARGETS_PATH.joinpath('HMS II.3 Harman over-ear 2018 without bass.csv'),
            'label': 'HMS II.3 Harman over-ear 2018',
            'compatible': [
                {'source': 'nebulabox', 'form': 'over-ear'},
                {'source': 'Headphone.com Legacy', 'form': 'over-ear'},
                {'source': 'Innerfidelity', 'form': 'over-ear'},
                {'source': 'Rtings', 'form': 'over-ear', 'rig': 'HMS II.3'},
            ],
            'recommended': [
                {'source': 'Headphone.com Legacy', 'form': 'over-ear'},
                {'source': 'Innerfidelity', 'form': 'over-ear'},
                {'source': 'Rtings', 'form': 'over-ear', 'rig': 'HMS II.3'},
            ],
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 6}
        },
        {
            'file': TARGETS_PATH.joinpath('JM-1 with Harman treble filter.csv'),
            'label': 'JM-1 with Harman filters',
            'compatible': [
                {'source': 'crinacle', 'form': 'in-ear', 'rig': 'Bruel & Kjaer 4620'},
                {'source': 'HypetheSonics', 'form': 'in-ear', 'rig': 'Bruel & Kjaer 5128'},
                {'source': 'Rtings', 'form': 'in-ear', 'rig': 'Bruel & Kjaer 5128'},
            ],
            'recommended': [
                {'source': 'crinacle', 'form': 'in-ear', 'rig': 'Bruel & Kjaer 4620'},
                {'source': 'HypetheSonics', 'form': 'in-ear', 'rig': 'Bruel & Kjaer 5128'},
                {'source': 'Rtings', 'form': 'in-ear', 'rig': 'Bruel & Kjaer 5128'},
            ],
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 6.5}
        },
        {
            'file': TARGETS_PATH.joinpath('LMG 5128 0.6 without bass.csv'),
            'compatible': [
                {'source': 'HypetheSonics', 'form': 'over-ear'},
                {'source': 'HypetheSonics', 'form': 'earbud'},
                {'source': 'Rtings', 'form': 'over-ear', 'rig': 'Bruel & Kjaer 5128'},
                {'source': 'Rtings', 'form': 'earbud', 'rig': 'Bruel & Kjaer 5128'},
            ],
            'recommended': [
                {'source': 'HypetheSonics', 'form': 'over-ear'},
                {'source': 'HypetheSonics', 'form': 'earbud'},
                {'source': 'Rtings', 'form': 'over-ear', 'rig': 'Bruel & Kjaer 5128'},
                {'source': 'Rtings', 'form': 'earbud', 'rig': 'Bruel & Kjaer 5128'},
            ],
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 6}
        },
    ]
    ####### [END] standard from dbtools ########

    ####### [BEGIN] add targets from nebulabox ########

    for csv_file in MEASUREMENTS_PATH.glob('nebulabox/data/**/*.csv'):
        new_target = {
            'file': Path(csv_file),
            'label': csv_file.name,
            'source' : 'nebulabox',
            'compatible': [
                {'source': 'nebulabox', 'form': 'over-ear'},
                {'source': 'nebulabox', 'form': 'in-ear'}
            ],
            'recommended': [],
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 0}
        }
        targets.append(new_target)
    # add all others
    # 使用 key=lambda x: x.name 确保只根据文件名排序
    sorted_files = sorted(MEASUREMENTS_PATH.glob('*/data/**/*.csv'), key=lambda x: x.name)
    for csv_file in sorted_files:
        source = csv_file.parts[csv_file.parts.index('data') - 1]
        if source == 'nebulabox':
            continue
        new_target = {
            'file': Path(csv_file),
            'label': csv_file.name.replace('.csv', ''),
            'source' : source,
            'bassBoost': {'fc': 105, 'q': 0.7, 'gain': 0}
        }
        targets.append(new_target)
    ####### [END] add targets from nebulabox ########

    for target in targets:
        if 'label' not in target:
            target['label'] = target['file'].name.replace('.csv', '')
        if 'compatible' not in target:
            target['compatible'] = []
        if 'recommended' not in target:
            target['recommended'] = []
        target['fr'] = FrequencyResponse.read_csv(target['file']).to_dict()
        del target['file']
    with open(WEBAPP_PATH.joinpath('data', 'targets.json'), 'w', encoding='utf-8') as fh:
        json.dump(targets, fh, ensure_ascii=False, indent=4)



def main():
    write_entries_and_measurements()
    write_targets()

if __name__ == '__main__':
    main()
