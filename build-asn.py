#!/usr/bin/env python3
import os
import json
import csv
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

# ASN data sources from Regional Internet Registries
ASN_SOURCES = {
    'apnic': 'https://ftp.apnic.net/stats/apnic/delegated-apnic-latest',
    'arin': 'https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest',
    'ripencc': 'https://ftp.ripe.net/ripe/stats/delegated-ripencc-latest',
    'afrinic': 'https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-latest',
    'lacnic': 'https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest'
}

class ASNEntry:
    def __init__(self, registry, country, asn, value, date, status):
        self.registry = registry
        self.country = country
        self.asn = asn
        self.value = value  # Number of ASNs allocated
        self.date = date
        self.status = status
    
    def to_dict(self):
        return {
            'Registry': self.registry,
            'Country': self.country,
            'ASN': self.asn,
            'Value': self.value,
            'Date': self.date,
            'Status': self.status
        }

def create_directories():
    """Create necessary directories for ASN data"""
    print('Creating ASN directories')
    directories = [
        'ASN',
        'ASN/CSV', 'ASN/CSV/BY_COUNTRY', 'ASN/CSV/BY_REGISTRY',
        'ASN/JSON', 'ASN/JSON/BY_COUNTRY', 'ASN/JSON/BY_REGISTRY',
        'ASN/TXT', 'ASN/TXT/BY_COUNTRY', 'ASN/TXT/BY_REGISTRY'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def process_asn_data(registry_name, data):
    """Process ASN data from a registry"""
    print(f'Processing ASN data for {registry_name}')
    asn_entries = []
    
    for line in data.split('\n'):
        if line and not line.startswith('#'):
            parts = line.strip().split('|')
            if len(parts) >= 7 and parts[2] == 'asn':
                registry = parts[0]
                country = parts[1]
                asn_type = parts[2]
                asn_number = parts[3]
                value = parts[4]
                date = parts[5]
                status = parts[6]
                
                if asn_type == 'asn' and (status == 'allocated' or status == 'assigned'):
                    asn_entries.append(ASNEntry(registry, country, asn_number, value, date, status))
    
    return asn_entries

def download_and_process_asn(registry_name, url):
    """Download and process ASN data for a specific registry"""
    print(f'Downloading ASN data from {registry_name}')
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        asn_entries = process_asn_data(registry_name, response.text)
        print(f'✓ Successfully processed {registry_name}: {len(asn_entries)} ASN entries')
        return asn_entries
    except Exception as e:
        print(f'✗ Error processing {registry_name}: {e}')
        return []

def export_global_asn_data(all_asn_data):
    """Export aggregated global ASN data"""
    print('Exporting Global ASN Data')
    
    # Sort by ASN number
    sorted_data = sorted(all_asn_data, key=lambda x: int(x.asn))
    data_dicts = [entry.to_dict() for entry in sorted_data]
    
    # CSV
    with open('ASN/CSV/global_asn.csv', 'w', newline='', encoding='utf-8') as f:
        if data_dicts:
            writer = csv.DictWriter(f, fieldnames=['Registry', 'Country', 'ASN', 'Value', 'Date', 'Status'])
            writer.writeheader()
            writer.writerows(data_dicts)
    
    # JSON
    with open('ASN/JSON/global_asn.json', 'w', encoding='utf-8') as f:
        json.dump(data_dicts, f, indent=2)
    
    # TXT (just ASN numbers)
    with open('ASN/TXT/global_asn.txt', 'w', encoding='utf-8') as f:
        asn_list = [entry.asn for entry in sorted_data]
        f.write('\n'.join(asn_list))

def export_by_country(all_asn_data):
    """Export ASN data grouped by country"""
    print('Exporting ASN Data by Country')
    
    # Group by country
    country_data = defaultdict(list)
    for entry in all_asn_data:
        country_data[entry.country].append(entry)
    
    # Export for each country
    for country, entries in country_data.items():
        if country and country != '*':  # Skip empty or wildcard countries
            # Sort by ASN number
            sorted_entries = sorted(entries, key=lambda x: int(x.asn))
            data_dicts = [entry.to_dict() for entry in sorted_entries]
            
            # CSV
            csv_path = f'ASN/CSV/BY_COUNTRY/{country}.csv'
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['Registry', 'Country', 'ASN', 'Value', 'Date', 'Status'])
                writer.writeheader()
                writer.writerows(data_dicts)
            
            # JSON
            json_path = f'ASN/JSON/BY_COUNTRY/{country}.json'
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data_dicts, f, indent=2)
            
            # TXT (just ASN numbers)
            txt_path = f'ASN/TXT/BY_COUNTRY/{country}.txt'
            with open(txt_path, 'w', encoding='utf-8') as f:
                asn_list = [entry.asn for entry in sorted_entries]
                f.write('\n'.join(asn_list))

def export_by_registry(all_asn_data):
    """Export ASN data grouped by registry"""
    print('Exporting ASN Data by Registry')
    
    # Group by registry
    registry_data = defaultdict(list)
    for entry in all_asn_data:
        registry_data[entry.registry].append(entry)
    
    # Export for each registry
    for registry, entries in registry_data.items():
        # Sort by ASN number
        sorted_entries = sorted(entries, key=lambda x: int(x.asn))
        data_dicts = [entry.to_dict() for entry in sorted_entries]
        
        # CSV
        csv_path = f'ASN/CSV/BY_REGISTRY/{registry}.csv'
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Registry', 'Country', 'ASN', 'Value', 'Date', 'Status'])
            writer.writeheader()
            writer.writerows(data_dicts)
        
        # JSON
        json_path = f'ASN/JSON/BY_REGISTRY/{registry}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data_dicts, f, indent=2)
        
        # TXT (just ASN numbers)
        txt_path = f'ASN/TXT/BY_REGISTRY/{registry}.txt'
        with open(txt_path, 'w', encoding='utf-8') as f:
            asn_list = [entry.asn for entry in sorted_entries]
            f.write('\n'.join(asn_list))

def export_summary(all_asn_data):
    """Export summary statistics"""
    print('Generating ASN Summary')
    
    # Calculate statistics
    total_asns = len(all_asn_data)
    by_country = defaultdict(int)
    by_registry = defaultdict(int)
    by_status = defaultdict(int)
    
    for entry in all_asn_data:
        by_country[entry.country] += 1
        by_registry[entry.registry] += 1
        by_status[entry.status] += 1
    
    summary = {
        'total_asns': total_asns,
        'by_country': dict(sorted(by_country.items(), key=lambda x: x[1], reverse=True)),
        'by_registry': dict(sorted(by_registry.items())),
        'by_status': dict(sorted(by_status.items())),
        'countries_count': len(by_country),
        'registries_count': len(by_registry)
    }
    
    # Save summary
    with open('ASN/JSON/summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    # Create a readable summary text
    with open('ASN/TXT/summary.txt', 'w', encoding='utf-8') as f:
        f.write(f'ASN Allocation Summary\n')
        f.write(f'=====================\n\n')
        f.write(f'Total ASNs: {total_asns:,}\n')
        f.write(f'Countries: {len(by_country)}\n')
        f.write(f'Registries: {len(by_registry)}\n\n')
        
        f.write(f'By Registry:\n')
        for registry, count in sorted(by_registry.items()):
            f.write(f'  {registry}: {count:,}\n')
        
        f.write(f'\nTop 10 Countries by ASN Count:\n')
        for country, count in list(sorted(by_country.items(), key=lambda x: x[1], reverse=True))[:10]:
            f.write(f'  {country}: {count:,}\n')

def main():
    """Main function to process ASN data"""
    # Create directories
    create_directories()
    
    # Download and process ASN data in parallel
    print('\n=== Downloading and Processing ASN Data ===')
    all_asn_data = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_registry = {
            executor.submit(download_and_process_asn, registry, url): registry 
            for registry, url in ASN_SOURCES.items()
        }
        
        for future in as_completed(future_to_registry):
            registry = future_to_registry[future]
            try:
                asn_entries = future.result()
                all_asn_data.extend(asn_entries)
            except Exception as e:
                print(f'✗ Error with {registry}: {e}')
    
    if not all_asn_data:
        print('No ASN data collected. Exiting.')
        return
    
    # Export data
    print('\n=== Exporting ASN Data ===')
    export_global_asn_data(all_asn_data)
    export_by_country(all_asn_data)
    export_by_registry(all_asn_data)
    export_summary(all_asn_data)
    
    print('\n✓ ASN build completed successfully!')
    
    # Display summary
    total_asns = len(all_asn_data)
    countries = len(set(entry.country for entry in all_asn_data if entry.country and entry.country != '*'))
    registries = len(set(entry.registry for entry in all_asn_data))
    
    print(f'\nSummary:')
    print(f'  - Total ASNs: {total_asns:,}')
    print(f'  - Countries: {countries}')
    print(f'  - Registries: {registries}')

if __name__ == '__main__':
    main()