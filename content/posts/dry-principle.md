---
title: "How Dry principle leads to clean and easy to debug code?"
date: 2020-06-17T18:54:08+01:00
draft: false
image: /images/flower.webp
thumbnail: /images/flower_tn.webp
tags: ['Design Pattern']
categories: "Design"
summary: "Dry is short for “Don’t repeat yourself”.
 There are occasions that a piece of code is rewritten several times.
 It is better to define that as a specific method or class.
 I explain it with examples."
---

## Introduction

Dry is short for “Don’t repeat yourself”.
 There are occasions that a piece of code is rewritten several times.
 It is better to define that as a specific method or class.
 I explain it with examples.

## Example 1

We have a car class which calculates momentum, air drag force and kinetic energy as below

```c#
public class Car
{
    public double Mass { get; set; }
    public double Acceleration { get; set; }
    public double InitialVelocity {get; set;}

    double ComputeMomentum(double time)
    {
        var velocity = (Acceleration * 0.098 * (time + Math.Log(time)) + 0.1 * time + InitialVelocity;
        return Mass * velocity;
    }

    double ComputeDragForce(double time)
    {
        var velocity = (Acceleration * 0.098 * (time + Math.Log(time)) + 0.1 * time + InitialVelocity;
        return 10 * velocity * velocity + 100;
    }

    double ComputeKineticEnergy(double time)
    {
        var velocity = (Acceleration * 0.098 * (time + Math.Log(time)) + 0.1 * time + InitialVelocity;
        return 0.5 * Mass * velocity * velocity;
    }
}
```

Both `ComputeMomentum` and `ComputeDragForce` methods calculate velocity
but the equation is repeated. There are two problems with this
approach: firstly, we usually write more than what we should.  
Secondly, it is prone to future bugs since sometime in future we may
want to change the velocity equation, then we have to find and then
change all equations.
To solve the issues we can do this

```C#
public class Car
{
    public double Mass { get; set; }

    double ComputeVelocity(double time)
    {
        var velocity = (Acceleration * 0.098 * (time + Math.Log(time)) + 0.1 * time + InitialVelocity;        
    }

    double ComputeMomentum(double time)
    {
        return Mass * ComputeVelocity(time);
    }

    double ComputeDragForce(double acceleration, double time, double initialVelocity)
    {
        var velocity = ComputeVelocity(time);
        return 10 * velocity * velocity + 100;
    }

    double ComputeKineticEnergy(double time)
    {
        var velocity = ComputeVelocity(time);
        return 0.5 * Mass * velocity * velocity;
    }
```

Now the way velocity is computed is hidden from other methods (encapsulation principle),
by changing `ComputeVelocity` definition, all other methods get the new correct value.
Moreover, it is simpler and cleaner to debug. Remember to name functions in a way that
they can be understood quickly (book Clean Code by R. C. Martin).
Generally, I do not recommend predicting every scenario and
creating unnecessary methods and wasting your time, but the moment you see
yourself repeating a piece of code like an equation,
or several lines with specific logic, immediately create a method out of it.

## Example 2

The example above was to extract a method and repeatedly use it in the same class.
But there are cases that a set of behaviours together are repeated among different classes.
Let's have a look at the below example

```C#
public class Data2D
{
	public double X { get; set; }
	public double Y { get; set; }
}
public class Locations
{
	private Data2D[] _data;

	public void Export(string fileName)
	{
		using (System.IO.StreamWriter file =
		new System.IO.StreamWriter(fileName))
		{
			for (int i = 0; i < _data.Length; i++)
			{
				file.WriteLine($"{ _data[i].X}, {_data[i].Y}");
			}
		}
	}
	// Rest of code
}

public class Velocities
{
	private Data2D[] _data;

	public void Export(string fileName)
	{
		using (System.IO.StreamWriter file =
		new System.IO.StreamWriter(fileName))
		{
			for (int i = 0; i < _data.Length; i++)
			{
				file.WriteLine($"{ _data[i].X}, {_data[i].Y}");
			}
		}
	}
	// Rest of code
}
```

In both `Locations` and `Velocities` classes, the `Export` method is repeated.
The method carries an independent responsibility of
dumping the array of `Data2D` into a desired file.
We can create a new class out of it to be used in similar scenarios.

```C#
public class Data2dExporter
{
	private Data2D[] _data;
	public Data2dExporter(Data2D[] data)
	{
		_data = data;
	}

	public void Export(string fileName)
	{
		using (System.IO.StreamWriter file =
		new System.IO.StreamWriter(fileName))
		{
			for (int i = 0; i < _data.Length; i++)
			{
				file.WriteLine($"{ _data[i].X}, {_data[i].Y}");
			}
		}
	}
}

public class Locations
{
	private Data2D[] _data;
	private Data2dExporter _data2DExporter;
	public Locations()
	{
		_data2DExporter = new Data2dExporter(_data);
	}
	public void Export(string fileName)
	{
		_data2DExporter.Export(fileName);
	}
	// Rest of code

}

public class Velocities
{
	private Data2D[] _data;
	private Data2dExporter _data2DExporter;
	public Velocities()
	{
		_data2DExporter = new Data2dExporter(_data);
	}
	public void Export(string fileName)
	{
		_data2DExporter.Export(fileName);
	}
	// Rest of code
}
```

Now both `Locations` and `Velocities` are using the logic we wrote in class `Data2dExporter`.
You might say we haven't saved in writing, actually, we wrote more in our DRY version.
However, firstly, we wrote `Data2dExporter` once and we can instantiate it in many other/new classes
without rewriting it. Secondly, if any logic of the exporter is changed in future, it will be fixed
in one place. Thirdly, `Data2dExporter` can now be extended to accommodate different implementations like
CSV and JSON exporter.
