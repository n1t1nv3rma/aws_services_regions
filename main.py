#from typing import Any
import httpx
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base

# Initialize FastMCP server
mcp = FastMCP("awsrands")

# Constants
NWS_API_BASE = "https://www.aws-services.info/"
USER_AGENT = "rands-app/1.0"

# Function to fetch list of all aws services and format output in table form
@mcp.tool()
async def aws_services() -> str:
    """
    Fetches list of all AWS services from the AWS Services website and formats the output as a table. 
    You can further reach out to your tool 'aws_regions_for_service' with "service_regions_url" as input URL to find list of all AWS regions a specific AWS services is available in, and when that AWS service was launched in that Region.
    Returns:
    str: A formatted table containing the list of AWS services with their names, service regions link, service product url, and the number of regions where this service is available.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(NWS_API_BASE + "services.html", headers={"User-Agent": USER_AGENT})
        response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    output = ""
    # Find the <p> tag that contains the <b> tag with "Updated on:"
    for p in soup.find_all('p'):
        b = p.find('b')
        if b and b.text.strip() == "Updated on:":
            # The text node directly after the <b> tag is what we want
            if b.next_sibling:
                updated_info = b.next_sibling.strip()
                #print("Updated on:", updated_info)
                output = f"This information was last updated on: {updated_info}\n"
                break

    table = soup.find('table', class_='table table-striped')
    rows = table.find_all('tr')

    services = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        service_name = cols[0].text.strip()
        # Find the anchor tag and extract href safely
        anchor_tag = cols[0].find('a')
        service_regions_url = NWS_API_BASE
        if anchor_tag and anchor_tag.get('href'):
            service_regions_url = NWS_API_BASE + anchor_tag.get('href')
        service_product_link = cols[1].text.strip() if cols[1].text.strip() else 'NA'
        regions = cols[2].text.strip()
        services.append([service_name, service_regions_url, service_product_link, regions])

    # Format the output as a table
    output += "\nService Name\t\tService in Regions URL\t\t Product Link\t\tNo. of Regions\n"
    output += "-" * 50 + "\n"
    for service in services:
        output += f"{service[0]}\t\t{service[1]}\t\t{service[2]}\t\t{service[3]}\n"

    return output

# Function to fetch list of all aws regions for a specific service and format output in table form
@mcp.tool()
async def aws_regions_for_service(service_regions_url) -> str:
    """
    Provides list of all AWS regions where a given AWS Service is available, and date when that Service was launched in the AWS regions.
    You MUST run your 'aws_services' tool to find the service URLs of all AWS Services. Refer to the "Service in Regions URL" from output of the "aws_services" tool to find the service URLs.
    Returns:
        str: A formatted table containing the list of AWS regions with their region code, region name and date of service release, and service product URL if there.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(service_regions_url, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    output = ""
    # Find the <p> tag that contains the <b> tag with "Updated on:"
    for p in soup.find_all('p'):
        b = p.find('b')
        if b and b.text.strip() == "Updated on:":
            # The text node directly after the <b> tag is what we want
            if b.next_sibling:
                updated_info = b.next_sibling.strip()
                #print("Updated on:", updated_info)
                output = f"This information was last updated on: {updated_info}\n"
                break
  
    # Use soup to find text between <font color="green"> and </font> element
    font_green = soup.find('font', color="green")
    if font_green:
        service_name = font_green.text.strip()
        # print(f"AWS service: '{service_name}' is currently available in following AWS Regions:\n")
        output += f"AWS service: '{service_name}' is currently available in following AWS Regions:\n"
    table = soup.find('table', class_='table table-striped')
    rows = table.find_all('tr')

    regions = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        region_code = cols[0].text.strip()
        aws_region_name = cols[1].text.strip()
        date_of_service_launched_in_region = cols[2].text.strip()
        service_product_link = cols[3].text.strip() if cols[3].text.strip() else 'NA'
        regions.append([region_code, aws_region_name, date_of_service_launched_in_region, service_product_link])

    # Format the output as a table
    output += "\nAWS Region Code\t\tAWS Service Name\t\tDate Of Service Launched In Regions\t\tService Product Link\n"
    output += "-" * 50 + "\n"
    for region in regions:
        output += f"{region[0]}\t\t{region[1]}\t\t{region[2]}\t\t{region[3]}\n"

    return output

# Function to fetch list of all aws regions and format output in table form
@mcp.tool()
async def aws_regions() -> str:
    """
    Fetches list of all AWS Regions and formats the output as a table.
    You can further reach out to your tool 'aws_services_in_region' with "region_services_url" as input URL to find list of all AWS services available in that Region, and when that AWS service was launched in that Region.
    Returns:
    str: A formatted table containing the list of AWS Regions with their AWS Region Name, AWS Region Code, URL link for more info, Number (count) of Unique AWS Services in that region, and Number (count) of AWS Availability Zones in that Region.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(NWS_API_BASE + "regions.html", headers={"User-Agent": USER_AGENT})
        response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    output = ""
    # Find the <p> tag that contains the <b> tag with "Updated on:"
    for p in soup.find_all('p'):
        b = p.find('b')
        if b and b.text.strip() == "Updated on:":
            # The text node directly after the <b> tag is what we want
            if b.next_sibling:
                updated_info = b.next_sibling.strip()
                #print("Updated on:", updated_info)
                output = f"This information was last updated on: {updated_info}\n"
                break
 
    table = soup.find('table', class_='table table-striped')
    rows = table.find_all('tr')

    regions = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        region_name = cols[0].text.strip()
        # Find the anchor tag and extract href safely
        anchor_tag = cols[0].find('a')
        region_services_url = NWS_API_BASE
        if anchor_tag and anchor_tag.get('href'):
            region_services_url = NWS_API_BASE + anchor_tag.get('href')
        region_code = cols[1].text.strip()
        no_of_aws_services = cols[2].text.strip()
        no_of_aws_availability_zone = cols[3].text.strip()
        regions.append([region_name, region_code, region_services_url, no_of_aws_services, no_of_aws_availability_zone])

    # Format the output as a table
    output += "\nRegion Name\t\tRegion Code\t\tServices In This Region URL\t\tNo. of AWS Services in Region\t\tNo. of AWS Availability Zones\n"
    output += "-" * 50 + "\n"
    for region in regions:
        output += f"{region[0]}\t\t{region[1]}\t\t{region[2]}\t\t{region[3]}\t\t{region[4]}\n"

    return output

# Function to fetch list of all aws regions for a specific service and format output in table form
@mcp.tool()
async def aws_services_in_region(regions_url) -> str:
    """
    Provides list of all AWS services in a specific AWS region, and date when that Service was launched in specific AWS region.
    You MUST run your 'aws_regions' tool to find the region URLs of all AWS Regions. Refer to the "Services In This Region URL" from output of the "aws_regions" tool to find the region URLs.
    Returns:
        str: A formatted table containing the list of AWS service, date of service release, and service product URL if there.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(regions_url, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    output = ""
    # Find the <p> tag that contains the <b> tag with "Updated on:"
    for p in soup.find_all('p'):
        b = p.find('b')
        if b and b.text.strip() == "Updated on:":
            # The text node directly after the <b> tag is what we want
            if b.next_sibling:
                updated_info = b.next_sibling.strip()
                #print("Updated on:", updated_info)
                output = f"This information was last updated on: {updated_info}\n"
                break
  
    # Use soup to find text between <font color="green"> and </font> element
    font_green = soup.find('font', color="green")
    if font_green:
        region_name = font_green.text.strip()
        # print(f"AWS region: '{region_name}' currently has following AWS Services available:\n")
        output += f"AWS region: '{region_name}' currently has following AWS Services available:\n"
    table = soup.find('table', class_='table table-striped')
    rows = table.find_all('tr')

    services = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        service_name = cols[0].text.strip()
        date_of_service_launched_in_region = cols[1].text.strip()
        service_product_link = cols[2].text.strip() if cols[2].text.strip() else 'NA'
        services.append([service_name, date_of_service_launched_in_region, service_product_link])

    # Format the output as a table
    output += "\nAWS Service Name\t\tDate Of Service Launched In Regions\t\tService Product Link\n"
    output += "-" * 50 + "\n"
    for service in services:
        output += f"{service[0]}\t\t{service[1]}\t\t{service[2]}\n"

    return output

# Function to fetch list of all AWS Local Zones and format output in table form 
@mcp.tool()
async def aws_localzones() -> str:
    """
    Fetches list of all AWS Local Zones from the AWS Services website and formats the output as a table.
    Returns:
    str: A formatted table containing the list of AWS Local Zones with their Country and its City name, AWS Local Zone's Code, Local Zone's parent AWS Region Name and Local Zone's parent AWS Region Code".
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(NWS_API_BASE + "local_zones.html", headers={"User-Agent": USER_AGENT})
        response.raise_for_status()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    output = ""
    # Find the <p> tag that contains the <b> tag with "Updated on:"
    for p in soup.find_all('p'):
        b = p.find('b')
        if b and b.text.strip() == "Updated on:":
            # The text node directly after the <b> tag is what we want
            if b.next_sibling:
                updated_info = b.next_sibling.strip()
                #print("Updated on:", updated_info)
                output = f"This information was last updated on: {updated_info}\n"
                break
 
    table = soup.find('table', class_='table table-striped')
    rows = table.find_all('tr')

    lzs = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        lz_country_city = cols[0].text.strip()
        lz_code_name = cols[1].text.strip()
        lz_parent_aws_region_name = cols[2].text.strip()
        lz_parent_aws_region_code = cols[3].text.strip()
        lzs.append([lz_country_city, lz_code_name, lz_parent_aws_region_name, lz_parent_aws_region_code])

    # Format the output as a table
    output += "\nAWS Local Zone Country(City)\t\tAWS Local Zone Code\t\tLocal Zone's Parent AWS Region Name\t\tParent AWS Region Code\n"
    output += "-" * 50 + "\n"
    for lz in lzs:
        output += f"{lz[0]}\t\t{lz[1]}\t\t{lz[2]}\t\t{lz[3]}\n"

    return output

# Function to fetch list newly released AWS services and format output in table form 
@mcp.tool()
async def aws_latest_services() -> str:
    """
    Fetches list of latest AWS Services in last 30 days and formats the output as a table.
    Returns:
    str: A formatted table containing the list of latest released AWS Services with their AWS Region Name (region code) and Date that service was released".
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(NWS_API_BASE + "whatsnew.html", headers={"User-Agent": USER_AGENT})
        response.raise_for_status()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    output = ""
    # Find the <p> tag that contains the <b> tag with "Updated on:"
    for p in soup.find_all('p'):
        b = p.find('b')
        if b and b.text.strip() == "Updated on:":
            # The text node directly after the <b> tag is what we want
            if b.next_sibling:
                updated_info = b.next_sibling.strip()
                #print("Updated on:", updated_info)
                output = f"This information was last updated on: {updated_info}\n"
                break
 
    table = soup.find('table', class_='table table-striped')
    rows = table.find_all('tr')

    latest_svcs = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        aws_service_name = cols[0].text.strip()
        aws_service_region = cols[1].text.strip()
        aws_service_release_date = cols[2].text.strip()
        latest_svcs.append([aws_service_name, aws_service_region,aws_service_release_date ])

    # Format the output as a table
    output += "\nAWS Service Released in Last 30 days\t\tCountry(City)\t\tService Launch Date\n"
    output += "+" * 50 + "\n"
    for svc in latest_svcs:
        output += f"{svc[0]}\t\t{svc[1]}\t\t{svc[2]}\n"

    return output

'''
# Send debug logs and notifications through the context
@mcp.tool()
async def process_debug_data(data: str, ctx: Context) -> str:
    """Process data with logging."""
    # Different log levels
    await ctx.debug(f"Debug: Processing '{data}'")
    # Notify about resource changes
    await ctx.session.send_resource_list_changed()
    return f"Processed: {data}"
'''

# MCP resources
@mcp.resource("resource://toolinfo")
async def region_and_services() -> str:
    """
    Returns information about list of tools available via this MCP server.
    """
    return "This service provides latest information about list of all AWS services and the AWS Regions they are running in. \n " \
    "You can use following tools to get specific information: \n " \
    "\tUse the tool 'aws_services' to get a list of AWS services with their names, and product url.\n" \
    "\tUse the tool 'aws_regions_for_service' with service_url as input to get list of all AWS Regions where that AWS service is available and when that AWS service was launched in that Region. \n" \
    "\tUse the tool 'aws_regions' to get a list of AWS Regions with their AWS Region Name, AWS Region Code, Number (count) of Unique AWS Services in that region, and Number (count) of AWS Availability Zones.\n" \
    "\tUse the tool 'aws_services_in_region' with region_services_url as input to get list of all AWS services available in that Region, and when that AWS service was launched in that Region. \n" \
    "\tUse the tool 'aws_localzones' to get list of AWS Local Zones with their Country and its City name, " \
    "AWS Local Zone's Code, Local Zone's parent AWS Region Name and Local Zone's parent AWS Region Code. " \
    "\tUse the tool 'aws_latest_services' to get list of latest AWS Services that are released within last 30 days " \
    "along with their AWS Region Name (region code) and Date that service was released."

@mcp.prompt(title="Default Prompt")
def default_prompt(query: str) -> str:
    return f"You have all the tools which can help you find out what AWS services are available in which regions or vice-versa. You can run recursive queries against the URI or URL in the initial response to further find out details on launch date of service in a region. Use your tools to solve all AWS regions or service related queries i.e. \n\n{query}"

@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I can help you list what AWS services are available in which regions or vice-versa:"),
        base.UserMessage(error),
        base.AssistantMessage("For example, You can ask: \n Which AWS Services are available in ap-southeast-2 region?, or, \n Which regions Amazon Bedrock service is available in?"),
    ]

"""
# For Local Testing:
if __name__ == "__main__":
    import asyncio
    #print(asyncio.run(aws_services()))
    print("\n\n")
    #print(asyncio.run(aws_regions_for_service('https://www.aws-services.info/apigateway.html')))
    print("@" * 50)
    #print(asyncio.run(aws_regions()))
    print("\n\n")
    #print(asyncio.run(aws_services_in_region('https://www.aws-services.info/af-south-1.html')))
    print("@" * 50)
    #print(asyncio.run(aws_localzones()))
    print("\n\n")
    print("@" * 50)
    #print(asyncio.run(aws_latest_services()))
"""

if __name__ == "__main__":
    #mcp.run(transport='streamable-http')
    mcp.run()
