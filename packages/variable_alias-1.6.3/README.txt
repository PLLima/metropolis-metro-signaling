Configures variable names from configuration files in the
package or project, or from the CodeName attribute.

The syntax of the CodeName attribute is '<pattern> <alias>' where
the pattern and space can be ommitted, giving the default pattern
'([^:])*:?(.*)' so that 'CodeName Eq["\1AS"] gives the same name as
'Alias Eq("$iAS")'.

Todo:

Remove, or make configurable, special cases from RB.
