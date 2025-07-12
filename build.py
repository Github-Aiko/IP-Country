#!/usr/bin/env python3
import os
import json
import csv
import requests
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import ipaddress

# Regional Internet Registries URLs
REGIONS_DELEGATED = {
    'delegated-apnic-latest': 'https://ftp.apnic.net/stats/apnic/delegated-apnic-latest',
    'delegated-arin-extended-latest': 'https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest',
    'delegated-ripencc-latest': 'https://ftp.ripe.net/ripe/stats/delegated-ripencc-latest',
    'delegated-afrinic-latest': 'https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-latest',
    'delegated-lacnic-latest': 'https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest'
}

class IPPackage:
    def __init__(self, country, ip, prefix_length, version):
        self.country = country
        self.ip = ip
        self.prefix_length = prefix_length
        self.version = version
    
    def to_dict(self):
        return {
            'Country': self.country,
            'IP': self.ip,
            'PrefixLength': self.prefix_length,
            'Version': self.version
        }

def create_directories():
    """Create necessary directories if they don't exist"""
    print('Creating directories')
    directories = [
        'IANASources',
        'CSV', 'CSV/IPV4', 'CSV/IPV6',
        'JSON', 'JSON/IPV4', 'JSON/IPV6',
        'TXT', 'TXT/IPV4', 'TXT/IPV6'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def download_region_data(region_name, url):
    """Download data for a specific region"""
    print(f'Downloading {region_name}')
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    file_path = f'IANASources/{region_name}.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    return region_name

def process_region_data(region_name):
    """Process downloaded region data"""
    print(f'Processing {region_name}')
    ip_data = []
    
    file_path = f'IANASources/{region_name}.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if 'allocated' in line or 'assigned' in line:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    registry = parts[0]
                    country = parts[1]
                    ip_type = parts[2]
                    ip_address = parts[3]
                    value = parts[4]
                    
                    if ip_type == 'ipv4' and value.isdigit():
                        # Calculate CIDR prefix length for IPv4
                        prefix_length = str(int(32 - math.log2(int(value))))
                        ip_data.append(IPPackage(country, ip_address, prefix_length, ip_type))
                    elif ip_type == 'ipv6' and value.isdigit():
                        # IPv6 prefix length is directly provided
                        ip_data.append(IPPackage(country, ip_address, value, ip_type))
    
    return ip_data

def sort_ip_data(ip_data):
    """Sort IP data by country, version, and IP address"""
    def ip_sort_key(package):
        if package.version == 'ipv4':
            # Convert IPv4 to integer for proper sorting
            try:
                ip_int = int(ipaddress.IPv4Address(package.ip))
            except:
                ip_int = 0
        else:
            # Convert IPv6 to integer for proper sorting
            try:
                ip_int = int(ipaddress.IPv6Address(package.ip))
            except:
                ip_int = 0
        return (package.country, package.version, ip_int)
    
    return sorted(ip_data, key=ip_sort_key)

def export_countries_list(sorted_data):
    """Export list of countries"""
    print('Exporting Countries Lists')
    countries = sorted(list(set(pkg.country for pkg in sorted_data)))
    
    # CSV
    with open('CSV/countries.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['country'])
        for country in countries:
            writer.writerow([country])
    
    # JSON
    countries_list = [{'country': country} for country in countries]
    with open('JSON/countries.json', 'w', encoding='utf-8') as f:
        json.dump(countries_list, f, indent=2)
    
    # TXT
    with open('TXT/countries.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(countries))

def export_global_data(sorted_data):
    """Export aggregated global data"""
    print('Exporting Aggregated Global Data')
    
    # Convert to list of dictionaries
    data_dicts = [pkg.to_dict() for pkg in sorted_data]
    
    # CSV
    with open('CSV/global.csv', 'w', newline='', encoding='utf-8') as f:
        if data_dicts:
            writer = csv.DictWriter(f, fieldnames=['Country', 'IP', 'PrefixLength', 'Version'])
            writer.writeheader()
            writer.writerows(data_dicts)
    
    # JSON
    with open('JSON/global.json', 'w', encoding='utf-8') as f:
        json.dump(data_dicts, f, indent=2)
    
    # JSON compressed
    with open('JSON/global_compressed.json', 'w', encoding='utf-8') as f:
        json.dump(data_dicts, f, separators=(',', ':'))

def export_version_specific_data(sorted_data, version):
    """Export data for specific IP version"""
    print(f'Exporting Global {version.upper()} Data')
    
    version_data = [pkg for pkg in sorted_data if pkg.version == version]
    data_dicts = [pkg.to_dict() for pkg in version_data]
    
    # CSV
    csv_path = f'CSV/global_{version}.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        if data_dicts:
            writer = csv.DictWriter(f, fieldnames=['Country', 'IP', 'PrefixLength', 'Version'])
            writer.writeheader()
            writer.writerows(data_dicts)
    
    # JSON
    json_path = f'JSON/global_{version}.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data_dicts, f, indent=2)
    
    # JSON compressed
    json_compressed_path = f'JSON/global_{version}_compressed.json'
    with open(json_compressed_path, 'w', encoding='utf-8') as f:
        json.dump(data_dicts, f, separators=(',', ':'))

def export_country_data(sorted_data):
    """Export data grouped by country"""
    print('Exporting Country-specific Data')
    
    # Group by country and version
    country_data = defaultdict(lambda: {'ipv4': [], 'ipv6': []})
    
    for pkg in sorted_data:
        country_data[pkg.country][pkg.version].append(pkg)
    
    # Export data for each country
    for country, versions in country_data.items():
        for version, packages in versions.items():
            if packages:
                # CSV
                csv_path = f'CSV/{version.upper()}/{country}.csv'
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['Country', 'IP', 'PrefixLength', 'Version'])
                    writer.writeheader()
                    writer.writerows([pkg.to_dict() for pkg in packages])
                
                # JSON
                json_path = f'JSON/{version.upper()}/{country}.json'
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump([pkg.to_dict() for pkg in packages], f, indent=2)
                
                # TXT (CIDR format)
                txt_path = f'TXT/{version.upper()}/{country}.txt'
                with open(txt_path, 'w', encoding='utf-8') as f:
                    cidr_list = [f'{pkg.ip}/{pkg.prefix_length}' for pkg in packages]
                    f.write('\n'.join(cidr_list))

def main():
    """Main function to orchestrate the entire process"""
    # Create directories
    create_directories()
    
    # Download data in parallel
    print('\n=== Downloading IANA Source Data ===')
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_region = {
            executor.submit(download_region_data, region, url): region 
            for region, url in REGIONS_DELEGATED.items()
        }
        
        for future in as_completed(future_to_region):
            region = future_to_region[future]
            try:
                result = future.result()
                print(f'✓ Successfully downloaded {result}')
            except Exception as e:
                print(f'✗ Error downloading {region}: {e}')
    
    # Process data
    print('\n=== Processing IANA Data ===')
    all_ip_data = []
    
    for region in REGIONS_DELEGATED.keys():
        try:
            region_data = process_region_data(region)
            all_ip_data.extend(region_data)
            print(f'✓ Processed {region}: {len(region_data)} entries')
        except Exception as e:
            print(f'✗ Error processing {region}: {e}')
    
    # Sort data
    print('\n=== Sorting IP Data ===')
    sorted_data = sort_ip_data(all_ip_data)
    print(f'Total entries: {len(sorted_data)}')
    
    # Export data
    print('\n=== Exporting Data ===')
    export_countries_list(sorted_data)
    export_global_data(sorted_data)
    export_version_specific_data(sorted_data, 'ipv4')
    export_version_specific_data(sorted_data, 'ipv6')
    export_country_data(sorted_data)
    
    print('\n✓ Build completed successfully!')
    
    # Summary statistics
    ipv4_count = sum(1 for pkg in sorted_data if pkg.version == 'ipv4')
    ipv6_count = sum(1 for pkg in sorted_data if pkg.version == 'ipv6')
    countries_count = len(set(pkg.country for pkg in sorted_data))
    
    print(f'\nSummary:')
    print(f'  - Total IPv4 blocks: {ipv4_count:,}')
    print(f'  - Total IPv6 blocks: {ipv6_count:,}')
    print(f'  - Total countries: {countries_count}')

if __name__ == '__main__':
    main()