from dataclasses import dataclass, field
from typing import List, Optional
import xml.etree.ElementTree as ET
from pathlib import Path

from CacheSync import CacheSync
import requests
import time
import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TransferSpeedColumn, BarColumn, TextColumn, TimeRemainingColumn, DownloadColumn
import zipfile
import shutil

# Create console instance
console = Console()

@dataclass
class ToolDependency:
    chocolatey_package_name: str
    version: str
    install_on_sut: bool
    install_on_host: bool
    package_parameters: Optional[str] = None
    owr_tool_name: Optional[str] = None
    executable_name: Optional[str] = None
    default_install_location: Optional[str] = None
    installer_name: Optional[str] = None


@dataclass
class ToolDependencies:
    dependencies: List[ToolDependency] = field(default_factory=list)
    
    @classmethod
    def from_xml_file(cls, file_path: str) -> "ToolDependencies":
        """Load tool dependencies from an XML file."""
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        dependencies = []
        
        for dep_elem in root.findall("ToolDependency"):
            # Required fields
            chocolatey_package_name = dep_elem.findtext("chocolateyPackageName")
            version = dep_elem.findtext("version")
            
            # Convert string booleans to actual booleans
            install_on_sut_text = dep_elem.findtext("installOnSut") or "False"
            install_on_host_text = dep_elem.findtext("installOnHost") or "False"
            
            install_on_sut = install_on_sut_text.lower() == "true"
            install_on_host = install_on_host_text.lower() == "true"
            
            # Optional fields
            package_parameters = dep_elem.findtext("packageParameters")
            owr_tool_name = dep_elem.findtext("OWRToolName")
            executable_name = dep_elem.findtext("executableName")
            default_install_location = dep_elem.findtext("defaultInstallLocation")
            installer_name = dep_elem.findtext("installerName")
            
            if chocolatey_package_name and version:
                dependency = ToolDependency(
                    chocolatey_package_name=chocolatey_package_name,
                    version=version,
                    install_on_sut=install_on_sut,
                    install_on_host=install_on_host,
                    package_parameters=package_parameters,
                    owr_tool_name=owr_tool_name,
                    executable_name=executable_name,
                    default_install_location=default_install_location,
                    installer_name=installer_name
                )
                dependencies.append(dependency)
        
        return cls(dependencies=dependencies)

    def to_xml_file(self, file_path: str) -> None:
        """Save tool dependencies to an XML file."""
        root = ET.Element("ToolDependencies")
        
        for dependency in self.dependencies:
            dep_elem = ET.SubElement(root, "ToolDependency")
            
            # Add optional elements if they exist
            if dependency.owr_tool_name:
                ET.SubElement(dep_elem, "OWRToolName").text = dependency.owr_tool_name
                
            ET.SubElement(dep_elem, "chocolateyPackageName").text = dependency.chocolatey_package_name
            
            if dependency.executable_name:
                ET.SubElement(dep_elem, "executableName").text = dependency.executable_name
                
            if dependency.default_install_location:
                ET.SubElement(dep_elem, "defaultInstallLocation").text = dependency.default_install_location
                
            if dependency.installer_name:
                ET.SubElement(dep_elem, "installerName").text = dependency.installer_name
                
            ET.SubElement(dep_elem, "version").text = dependency.version
            ET.SubElement(dep_elem, "installOnSut").text = str(dependency.install_on_sut)
            ET.SubElement(dep_elem, "installOnHost").text = str(dependency.install_on_host)
            
            if dependency.package_parameters is not None:
                ET.SubElement(dep_elem, "packageParameters").text = dependency.package_parameters
        
        # Create XML tree and write to file
        tree = ET.ElementTree(root)
        
        # Add XML declaration
        tree.write(file_path, encoding="utf-8", xml_declaration=True)


def download_artifact(path, directory = "package-dump" ): # Set the directory where files will be saved):
    console.print(path)
    downloadPath = CacheSync.DOWNLOAD_API.format(artifact_path=path)
    console.print(downloadPath)
    
    # Download the file using requests
    response = requests.get(downloadPath, stream=True)
    # Before starting the download
    start_time = time.time()

    if response.status_code == 200:
        # Create a filename from the package name and version
        
        Path(directory).mkdir(exist_ok=True)  # Create directory if it doesn't exist
        download_filename = str(Path(directory) / f"{package.chocolatey_package_name}.{package.version}.nupkg")
        # Check if file already exists
        if os.path.exists(download_filename):
            console.print(f"Skipping download: {download_filename} already exists", style="blue")
            return download_filename
        else:
            # Save the downloaded file
            # Get file size if available
            total_size = int(response.headers.get('content-length', 0))
            
            with Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.0f}%",
                "•",
                DownloadColumn(),
                "•",
                TransferSpeedColumn(),
                "•",
                TimeRemainingColumn()
            ) as progress:
                download_task = progress.add_task(f"[cyan]Downloading {package.chocolatey_package_name}", total=total_size)
                
                with open(download_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive chunks
                            f.write(chunk)
                            progress.update(download_task, advance=len(chunk))
            
            end_time = time.time()
            download_time = end_time - start_time
            file_size = os.path.getsize(download_filename)
            # Format file size for readability
            if file_size < 1024:
                size_str = f"{file_size} bytes"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size/1024:.2f} KB"
            else:
                size_str = f"{file_size/(1024*1024):.2f} MB"
            
            console.print(f"Downloaded to {download_filename}", style="green")
            console.print(f"File size: {size_str}, Download time: {download_time:.2f} seconds", style="green")
            return download_filename
    else:
        console.print(f"Failed to download: HTTP {response.status_code}", style="bold red")
        return None


def extract_artifact(artifact_path, directory = "package-dump", keep_artifact=True):
     if artifact_path:
            # Create extraction directory based on package name
            extract_dir = os.path.join(directory, f"{package.chocolatey_package_name}")
            Path(extract_dir).mkdir(exist_ok=True)
            
            console.print(f"Extracting {os.path.basename(artifact_path)} to {extract_dir}...", style="cyan")
            
            try:
                with zipfile.ZipFile(artifact_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                console.print(f"Successfully extracted package to {extract_dir}", style="green")
                
            except Exception as e:
                console.print(f"Failed to extract package: {str(e)}", style="bold red")  # Set the directory where files will be saved)
                return None
            if not keep_artifact:
                try:
                    if os.path.exists(artifact_path):
                        os.remove(artifact_path)
                        console.print(f"Deleted artifact file: {artifact_path}", style="blue")
                    else:
                        console.print(f"Artifact file not found: {artifact_path}", style="yellow")
                except Exception as e:
                    console.print(f"Failed to delete artifact file: {str(e)}", style="bold red")
                    return None
            return extract_dir

def cleaup_extracted_artifact(extracted_path):
    """
    Walks through the extracted directory and keeps only .nuspec and .ps1 files.
    Removes all other files and empty directories.
    """
    if not extracted_path or not os.path.exists(extracted_path):
        console.print(f"Invalid or missing extracted path: {extracted_path}", style="bold red")
        return
    
    console.print(f"Cleaning up extracted artifacts in {extracted_path}...", style="cyan")
    
    files_kept = 0
    files_removed = 0
    dirs_removed = 0
    
    # First pass: Delete unwanted files
    for root, dirs, files in os.walk(extracted_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.nuspec') or file.endswith('.ps1') or file.endswith('.txt'):
                files_kept += 1
            else:
                try:
                    os.remove(file_path)
                    console.print(f"      Deleting.. {file}", style="dim")
                    files_removed += 1
                except Exception as e:
                    console.print(f"Failed to remove file {file_path}: {str(e)}", style="bold red")
    
    # Second pass: Remove empty directories
    for root, dirs, files in os.walk(extracted_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                # Check if directory is empty
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    dirs_removed += 1
            except Exception as e:
                console.print(f"Failed to remove directory {dir_path}: {str(e)}", style="bold red")
    
    console.print(f"Cleanup completed: Kept {files_kept} files, removed {files_removed} files and {dirs_removed} directories.", style="green")

def copy_to_git(extracted_path):
    manual_dir = "manual"
    Path(manual_dir).mkdir(exist_ok=True)

    # Target destination path
    manual_path = os.path.join(manual_dir, os.path.basename(extracted_path))

    # Copy the extracted directory to manual folder
    console.print(f"Copying {extracted_path} to {manual_path}...", style="cyan")
    try:
        if os.path.exists(manual_path):
            shutil.rmtree(manual_path)  # Remove if already exists
        shutil.copytree(extracted_path, manual_path)
        console.print(f"Successfully copied to {manual_path}", style="green")
    except Exception as e:
        console.print(f"Failed to copy extracted files: {str(e)}", style="bold red")

# Example usage:
if __name__ == "__main__":
    
    # Parse from XML
    file_path = Path("c:/workspace/frameworks.validation.platform-automation.rails-shared/src/rails_shared/ToolDependencies.xml")
    tool_dependencies = ToolDependencies.from_xml_file(str(file_path))
    api = CacheSync()
    # Print number of dependencies
    console.print(f"Loaded {len(tool_dependencies.dependencies)} tool dependencies", style="bold green")
    
    # Example: Print all chocolatey packages that need to be installed on host
    # host_packages = [dep for dep in tool_dependencies.dependencies if dep.install_on_host]
    host_packages = tool_dependencies.dependencies

    console.print(f"Found {len(host_packages)} packages to install on host:", style="cyan")
    
    for idx, package in enumerate(host_packages[:10], 1):
        console.print(f"  [{idx}] - {package.chocolatey_package_name} (v{package.version})", style="yellow")
        path = api.get_artifact_path(CacheSync.SEARCH_ARTIFACTORY_URL, CacheSync.SEARCH_ARTIFACTORY_REPO, package.chocolatey_package_name, package.version)
        artifact_path = download_artifact(path)
        extracted_path = extract_artifact(artifact_path, keep_artifact=False)
        cleaup_extracted_artifact(extracted_path)
        copy_to_git(extracted_path=extracted_path)