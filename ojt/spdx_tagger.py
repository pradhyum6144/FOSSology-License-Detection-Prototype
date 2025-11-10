"""
SPDX Tagging Module
Generates SPDX-compliant license identifiers and tags
"""

import json
from typing import Dict, List, Optional

class SPDXTagger:
    """Handles SPDX license tagging and document generation"""
    
    def __init__(self, spdx_db_path: str = 'data/spdx_licenses.json'):
        """Initialize with SPDX license database"""
        self.spdx_db = self._load_spdx_db(spdx_db_path)
    
    def _load_spdx_db(self, path: str) -> Dict:
        """Load SPDX license database"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_spdx_db()
    
    def _get_default_spdx_db(self) -> Dict:
        """Default SPDX license information"""
        return {
            'MIT': {
                'id': 'MIT',
                'name': 'MIT License',
                'osi_approved': True,
                'fsf_libre': True,
                'url': 'https://spdx.org/licenses/MIT.html'
            },
            'Apache-2.0': {
                'id': 'Apache-2.0',
                'name': 'Apache License 2.0',
                'osi_approved': True,
                'fsf_libre': True,
                'url': 'https://spdx.org/licenses/Apache-2.0.html'
            },
            'GPL-2.0': {
                'id': 'GPL-2.0',
                'name': 'GNU General Public License v2.0',
                'osi_approved': True,
                'fsf_libre': True,
                'url': 'https://spdx.org/licenses/GPL-2.0.html'
            },
            'GPL-3.0': {
                'id': 'GPL-3.0',
                'name': 'GNU General Public License v3.0',
                'osi_approved': True,
                'fsf_libre': True,
                'url': 'https://spdx.org/licenses/GPL-3.0.html'
            },
            'BSD-3-Clause': {
                'id': 'BSD-3-Clause',
                'name': 'BSD 3-Clause License',
                'osi_approved': True,
                'fsf_libre': True,
                'url': 'https://spdx.org/licenses/BSD-3-Clause.html'
            },
            'LGPL-2.1': {
                'id': 'LGPL-2.1',
                'name': 'GNU Lesser General Public License v2.1',
                'osi_approved': True,
                'fsf_libre': True,
                'url': 'https://spdx.org/licenses/LGPL-2.1.html'
            }
        }
    
    def get_spdx_info(self, license_name: str) -> Dict:
        """
        Get SPDX information for a license
        
        Args:
            license_name: Name or identifier of the license
        
        Returns:
            Dictionary with SPDX information
        """
        # Try to find by name or ID
        for spdx_id, info in self.spdx_db.items():
            if license_name.lower() in info['name'].lower() or license_name == spdx_id:
                return {
                    'spdx_id': info['id'],
                    'name': info['name'],
                    'osi_approved': info.get('osi_approved', False),
                    'fsf_libre': info.get('fsf_libre', False),
                    'url': info.get('url', ''),
                    'found': True
                }
        
        return {
            'spdx_id': None,
            'name': license_name,
            'osi_approved': False,
            'fsf_libre': False,
            'url': '',
            'found': False
        }
    
    def generate_spdx_document(self, results: List[Dict]) -> str:
        """
        Generate SPDX-formatted document from analysis results
        
        Args:
            results: List of detection results
        
        Returns:
            SPDX-formatted string
        """
        lines = [
            'SPDXVersion: SPDX-2.3',
            'DataLicense: CC0-1.0',
            'SPDXID: SPDXRef-DOCUMENT',
            'DocumentName: License Detection Report',
            'DocumentNamespace: https://example.com/license-detection',
            '',
            '## Package Information',
            ''
        ]
        
        # Group by license
        license_groups = {}
        for result in results:
            spdx_id = result.get('spdx_id', 'NOASSERTION')
            if spdx_id not in license_groups:
                license_groups[spdx_id] = []
            license_groups[spdx_id].append(result)
        
        # Generate package entries
        package_num = 1
        for spdx_id, group in license_groups.items():
            lines.append(f'## Package {package_num}')
            lines.append(f'PackageName: Fragment-{package_num}')
            lines.append(f'SPDXID: SPDXRef-Package-{package_num}')
            lines.append(f'PackageLicenseDeclared: {spdx_id}')
            lines.append(f'PackageLicenseConcluded: {spdx_id}')
            lines.append(f'PackageCopyrightText: NOASSERTION')
            lines.append(f'PackageComment: Detected with confidence {group[0].get("confidence", 0)}')
            lines.append('')
            package_num += 1
        
        lines.append('## Extracted Licenses')
        lines.append('')
        
        # List unique licenses
        unique_licenses = set()
        for result in results:
            spdx_id = result.get('spdx_id')
            if spdx_id and spdx_id != 'NOASSERTION':
                unique_licenses.add(spdx_id)
        
        for idx, spdx_id in enumerate(sorted(unique_licenses), 1):
            info = self.get_spdx_info(spdx_id)
            lines.append(f'LicenseID: LicenseRef-{spdx_id}')
            lines.append(f'ExtractedText: {info.get("name", spdx_id)}')
            lines.append('')
        
        return '\n'.join(lines)

