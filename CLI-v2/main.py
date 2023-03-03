from typing import Optional
import typer
import requests
from dataclasses import dataclass
import os

app = typer.Typer()

base_url ='http://ec2-52-207-76-7.compute-1.amazonaws.com:8000/docs'



@app.command()
def create_user(
    username: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(
        ..., prompt=True, confirmation_prompt=True, hide_input=True
    ),
    plan: int = typer.Option(..., prompt=True, help="Enter Plan No. to activate (1 - Free, 2 - Gold, 3 - Platinium)")
):
    """
    Create a new user.
    """
    data = {
            "username": username,
            "email": email,
            "password": password,
            "planId": plan
        }
    response = requests.post(f'{base_url}/user/sign-up', json=data)

    if response.status_code == 201:
        typer.echo("User created successfully! ✅")
    elif response.status_code == 409:
        typer.echo("User with the username and email already exists! 😐")
    elif response.status_code == 422:
        typer.echo(f"Oh-no! 😐: {response.json()['detail'][0]['msg']}")


@app.command()
def login(
    username:str = typer.Option(..., prompt=True),
    password: str = typer.Option(
        ..., prompt=True, hide_input=True
    )
):
    delete_token()
    # Command for user's login
    form_data = {
        "username": username,
        "password": password
    }
    response = requests.post(f'{base_url}/user/login', data=form_data)

    result = response.json()

    if response.status_code == 200:
        store_token(result['access_token'])
        typer.echo("User logged in successfully! ✅")

    elif response.status_code == 401:
        typer.echo("Invalid user credentials! ❌")

    elif response.status_code == 404:
        typer.echo("User not found! ❌")

    else:
        typer.echo(f"Oh-no! 😐: {response.json()['detail'][0]['msg']}")

@app.command()
def logout():

    token = get_token()
    if len(token) <= 0:
        print("You are not logged in!")
        raise typer.Abort()

    logout = typer.confirm("Are you sure you want to logout?")
    if not logout:
        print("Not action required! (Still logged in!)")
        raise typer.Abort()
    
    print("Signing off...")

    delete_token()
    print("Signed out! ✅")


@app.command()
def download_file(filename: str, bucket_name: str = typer.Option(..., "--bucket", '-b', help="Please specify bucker name (GOES/NEXRAD)")):
    """
    Download a file by name.
    """

    if bucket_name not in ['GOES', 'NEXRAD']:
         typer.echo(f"Please specify bucker name (GOES/NEXRAD)")
         raise typer.Exit()

    token = get_token()
    
    if len(token) <= 0:
        typer.echo("Please login first to get the file link!")

    else:
        if bucket_name == 'GOES':
            response = requests.post(f"{base_url}/goes/generate/aws-link-by-filename/{filename}", headers={"Authorization":f"Bearer {token}"})  
        else:
            response = requests.post(f"{base_url}/nexrad/generate/aws-link-by-filename/{filename}", headers={"Authorization":f"Bearer {token}"})  

        data = response.json()

        if response.status_code == 201:
            typer.echo(f"Downloadable file link: {data['our_bucket_link']}")
        
        elif response.status_code == 404:
            typer.echo(f"File with name {filename} not found!")

        elif response.status_code == 503:
            typer.echo(f"API limit reached! Please upgrade to higher plan.")

        elif response.status_code == 400:
            typer.echo(f"Invalid file with name: {filename} for Bucket: {bucket_name}")


@app.command()
def fetch_goes_files(
        station: str = typer.Option(..., prompt=True),
        year: int = typer.Option(..., prompt=True),
        day_of_year: str = typer.Option(..., prompt=True),
        hour_of_day: str = typer.Option(..., prompt=True),):
    """
    List all files in a bucket with the given prefix.
    """   
    token = get_token()
    if len(token) <= 0:
        typer.echo("Please login first to fetch the files!")

    else:

        response = requests.get(f"{base_url}/goes/files?station={station}&year={year}&day={day_of_year}&hour={hour_of_day}", headers={"Authorization":f"Bearer {token}"})  

        data = response.json()

        if response.status_code == 200:
            files:list = data['all_files']
            if len(files) == 0:
                typer.echo("There are no files available.")
                raise typer.Exit()
            else:
                for file in files:
                    typer.echo(file)


        elif response.status_code == 503:
            typer.echo(f"API limit reached! Please upgrade to higher plan.")

@app.command()
def fetch_nexrad_files(
        station: str = typer.Option(..., prompt=True),
        year: int = typer.Option(..., prompt=True),
        day_of_year: str = typer.Option(..., prompt=True),
        month_of_year: str = typer.Option(..., prompt=True),):
    """
    List all files in a bucket with the given prefix.
    """   
    token = get_token()
    if len(token) <= 0:
        typer.echo("Please login first to fetch the files!")

    else:

        response = requests.get(f"{base_url}/nexrad/files?stationId={station}&year={year}&day={day_of_year}&month={month_of_year}", headers={"Authorization":f"Bearer {token}"})  

        data = response.json()

        if response.status_code == 200:
            files:list = data['all_files']
            if len(files) == 0:
                typer.echo("There are no files available.")
                raise typer.Exit()
            else:
                for file in files:
                    typer.echo(file)


        elif response.status_code == 503:
            typer.echo(f"API limit reached! Please upgrade to higher plan.")


def store_token(token:str):
    with open("./data/config", "w") as text_file:
        text_file.write(token)
        text_file.close()

def get_token():
    with open("./data/config", "r") as text_file:
        data = text_file.read()
        text_file.close()

    return data

def delete_token():
    f = open("./data/config", "r+") 
    f.seek(0) 
    f.truncate() 


if __name__ == "__main__":
    app()