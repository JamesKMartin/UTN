< !DOCTYPE
html >
< html >
< head >
< meta
name = "viewport"
content = "width=device-width, initial-scale=1" >
< style >
body
{
    margin: 0;
font - family: Arial, Helvetica, sans - serif;
}

.topnav
{
    overflow: hidden;
background - color:  # 333;
}

.topnav
a
{
    float: left;
color:  # f2f2f2;
text - align: center;
padding: 14
px
16
px;
text - decoration: none;
font - size: 17
px;
}

.topnav
a: hover
{
    background - color:  # ddd;
        color: black;
}

.topnav
a.active
{
    background - color:  # 04AA6D;
        color: white;
}
< / style >
< style >
form
{
    width: 600px;
margin: 0
auto;
}
< / style >
< / head >
< body >

< div


class ="topnav" >

< a


class ="active" href="#home" > Home < / a >

< / div >

< div
style = "padding-left:16px" >

< form >
< fieldset >
< legend > Seats
reserved < / legend >

{ %
for seat in seats %}
if ({{seat[2]}} == 'is_reserved'){
< input type="checkbox" id="{{seat[2]}}" name="interest" value="other" onclick = myFunction() / >
{{seat[2]}} == 'not_reserved'
< label for ="other" > {{seat[0], seat[1], seat[2]}} < / label >

}
{ % endfor %}
< / fieldset >
< / form >
< p
id = "text"
style = "display:none" > Seats
are
cancelled! < / p >